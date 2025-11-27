from typing import Optional

import httpx

from app.core.logger import get_logger
from app.db.models import WeatherData

logger = get_logger(__name__)


class WeatherAPI:
    """Small wrapper around OpenWeatherMap API."""

    def __init__(self, api_key: str, units: str = "metric"):
        self.api_key = api_key
        self.units = units

    async def fetch_weather(self, city: str) -> WeatherData:
        if not self.api_key or self.api_key == "change-me":
            logger.warning("OpenWeather API key is not configured, using mock weather data")
            return WeatherData(condition="Sunny", temperature=21.0, description="Mocked data")

        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {"q": city, "appid": self.api_key, "units": self.units}

        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
            payload = response.json()
            return self._parse_payload(payload)
        except httpx.HTTPError as exc:
            logger.exception("Failed to fetch weather: %s", exc)
            return WeatherData(condition="Unknown", temperature=0.0, description="fallback after error")

    def _parse_payload(self, payload: dict) -> WeatherData:
        weather: Optional[dict] = None
        if payload.get("weather"):
            weather = payload["weather"][0]
        condition = weather.get("main") if weather else "Unknown"
        description = weather.get("description") if weather else None
        main_info = payload.get("main", {})
        temperature = float(main_info.get("temp", 0))
        logger.info("Fetched weather: %s %.1fC", condition, temperature)
        return WeatherData(condition=condition, temperature=temperature, description=description)
