from typing import List

from app.planner.activities import date, hiking, sport, studying
from app.planner.activities.base import BaseActivity
from .base import WeatherStrategy


class SunnyWeatherStrategy(WeatherStrategy):
    def base_activities(self) -> List[BaseActivity]:
        return [
            hiking.HIKING,
            sport.SPORT,
            date.DATE,
            studying.STUDYING,
        ]
