from typing import List, Optional

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.core.logger import get_logger
from app.db.models import Plan, UserPreferences
from app.planner.day_planner import DayPlanner
from app.weather.weather_station import WeatherStation

logger = get_logger(__name__)
router = APIRouter()
templates = Jinja2Templates(directory="templates")


def get_services(request: Request) -> tuple[DayPlanner, WeatherStation]:
    return request.app.state.planner, request.app.state.weather_station


@router.get("/health")
async def healthcheck() -> dict:
    return {"status": "ok"}


@router.get("/plan", response_model=Plan)
async def current_plan(
    user_id: str = "default", services: tuple[DayPlanner, WeatherStation] = Depends(get_services)
) -> Plan:
    planner, station = services
    plan = await planner.get_latest_plan(user_id)
    if not plan:
        weather = await station.check_weather(force=True)
        plan = await planner.update(weather, user_id=user_id)
    return plan


@router.post("/plan/refresh", response_model=Plan)
async def refresh_plan(
    user_id: str = "default",
    city: Optional[str] = None,
    services: tuple[DayPlanner, WeatherStation] = Depends(get_services),
) -> Plan:
    planner, station = services
    if city:
        station.set_city(city)
    weather = await station.check_weather(force=True)
    plan = await planner.update(weather, user_id=user_id)
    return plan


@router.get("/preferences/{user_id}", response_model=UserPreferences)
async def get_preferences(
    user_id: str, services: tuple[DayPlanner, WeatherStation] = Depends(get_services)
) -> UserPreferences:
    planner, _ = services
    return await planner.get_preferences(user_id)


@router.put("/preferences/{user_id}", response_model=UserPreferences)
async def update_preferences(
    user_id: str,
    preferences: UserPreferences,
    services: tuple[DayPlanner, WeatherStation] = Depends(get_services),
) -> UserPreferences:
    planner, _ = services
    return await planner.set_preferences(user_id, preferences)


@router.get("/plans", response_model=List[Plan])
async def list_plans(
    limit: int = 10,
    user_id: str = "default",
    services: tuple[DayPlanner, WeatherStation] = Depends(get_services),
) -> List[Plan]:
    planner, _ = services
    return await planner.list_plans(user_id=user_id, limit=limit)


@router.get("/", response_class=HTMLResponse)
async def index(
    request: Request,
    user_id: str = "default",
    services: tuple[DayPlanner, WeatherStation] = Depends(get_services),
) -> HTMLResponse:
    planner, station = services
    plan = await planner.get_latest_plan(user_id)
    if not plan:
        weather = await station.check_weather(force=True)
        plan = await planner.update(weather, user_id=user_id)
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "plan": plan,
        },
    )
