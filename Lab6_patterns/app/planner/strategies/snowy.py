from typing import List

from app.planner.activities import housework, sport, studying
from app.planner.activities.base import BaseActivity
from .base import WeatherStrategy


class SnowyWeatherStrategy(WeatherStrategy):
    def base_activities(self) -> List[BaseActivity]:
        return [
            studying.STUDYING,
            housework.HOUSEWORK,
            sport.SPORT,
        ]
