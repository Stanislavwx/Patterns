from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.routes import router
from app.core.config import get_settings
from app.core.logger import get_logger
from app.db.mongodb import close_client, get_database
from app.planner.day_planner import DayPlanner
from app.tasks.scheduler import WeatherScheduler
from app.weather.weather_api import WeatherAPI
from app.weather.weather_station import WeatherStation

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    db = get_database()
    planner = DayPlanner(db, settings.default_city)
    weather_api = WeatherAPI(settings.openweather_api_key)
    station = WeatherStation(weather_api, settings.default_city)
    station.subscribe(planner)
    scheduler = WeatherScheduler(station, settings.weather_poll_interval)
    scheduler.start()

    app.state.db = db
    app.state.planner = planner
    app.state.weather_station = station
    app.state.scheduler = scheduler

    logger.info("Application startup completed")
    try:
        # prime first plan so UI is not empty
        await station.check_weather(force=True)
        yield
    finally:
        logger.info("Shutting down application")
        await station.stop()
        await close_client()


app = FastAPI(title="Smart Day Planner", lifespan=lifespan)
app.include_router(router)
app.mount("/static", StaticFiles(directory="static"), name="static")
