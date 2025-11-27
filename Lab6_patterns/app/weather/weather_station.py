import asyncio
from contextlib import suppress
from typing import List, Protocol

from app.core.logger import get_logger
from app.db.models import WeatherData
from app.weather.weather_api import WeatherAPI

logger = get_logger(__name__)


class WeatherObserver(Protocol):
    async def update(self, weather: WeatherData) -> None:
        ...


class WeatherStation:
    """Observable that fetches weather updates and notifies observers."""

    def __init__(self, api: WeatherAPI, city: str):
        self.api = api
        self.city = city
        self.observers: List[WeatherObserver] = []
        self._running = False
        self._task: asyncio.Task | None = None
        self._last_condition: str | None = None

    def subscribe(self, observer: WeatherObserver) -> None:
        # Підписує спостерігача на зміни погоди
        if observer not in self.observers:
            self.observers.append(observer)

    def unsubscribe(self, observer: WeatherObserver) -> None:
        # Відписує спостерігача
        if observer in self.observers:
            self.observers.remove(observer)

    async def notify(self, weather: WeatherData) -> None:
        # Розсилає оновлені дані погоди всім спостерігачам
        for observer in list(self.observers):
            try:
                await observer.update(weather)
            except Exception:
                logger.exception("Observer %s failed to handle weather update", observer)

    async def check_weather(self, force: bool = False) -> WeatherData:
        weather = await self.api.fetch_weather(self.city)
        changed = weather.condition != self._last_condition
        self._last_condition = weather.condition
        if force or changed:
            logger.info("Weather changed or forced update: %s", weather.condition)
            await self.notify(weather)
        else:
            logger.debug("Weather unchanged: %s", weather.condition)
        return weather

    async def _run_loop(self, interval_seconds: int) -> None:
        self._running = True
        while self._running:
            try:
                await self.check_weather()
            except asyncio.CancelledError:
                break
            except Exception:
                logger.exception("Error during scheduled weather check")
            await asyncio.sleep(interval_seconds)

    def start(self, interval_seconds: int) -> None:
        if self._task and not self._task.done():
            return
        logger.info("Starting weather polling every %ss", interval_seconds)
        self._task = asyncio.create_task(self._run_loop(interval_seconds))

    async def stop(self) -> None:
        self._running = False
        if self._task:
            self._task.cancel()
            with suppress(asyncio.CancelledError):
                await self._task
            self._task = None

    def set_city(self, city: str) -> None:
        self.city = city
        logger.info("WeatherStation city set to %s", city)
