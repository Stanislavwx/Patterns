import asyncio
from contextlib import suppress

from app.core.logger import get_logger
from app.weather.weather_station import WeatherStation

logger = get_logger(__name__)


class WeatherScheduler:
    """Lightweight scheduler based on asyncio.create_task."""

    def __init__(self, station: WeatherStation, interval_seconds: int):
        self.station = station
        self.interval_seconds = interval_seconds
        self._task: asyncio.Task | None = None

    def start(self) -> None:
        self.station.start(self.interval_seconds)
        self._task = self.station._task  # reuse station loop

    async def stop(self) -> None:
        await self.station.stop()
        if self._task:
            with suppress(asyncio.CancelledError):
                await self._task
            self._task = None
