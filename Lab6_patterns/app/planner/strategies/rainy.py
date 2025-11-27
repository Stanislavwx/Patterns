from typing import List

from app.planner.activities import date, housework, studying
from app.planner.activities.base import BaseActivity
from .base import WeatherStrategy


class RainyWeatherStrategy(WeatherStrategy):
    def base_activities(self) -> List[BaseActivity]:
        return [
            housework.HOUSEWORK,
            studying.STUDYING,
            date.DATE,
        ]
