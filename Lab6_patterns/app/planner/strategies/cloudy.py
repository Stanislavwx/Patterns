from typing import List

from app.planner.activities import hiking, housework, studying
from app.planner.activities.base import BaseActivity
from .base import WeatherStrategy


class CloudyWeatherStrategy(WeatherStrategy):
    def base_activities(self) -> List[BaseActivity]:
        return [
            studying.STUDYING,
            hiking.HIKING,
            housework.HOUSEWORK,
        ]
