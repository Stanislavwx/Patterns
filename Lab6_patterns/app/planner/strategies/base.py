from abc import ABC, abstractmethod
from datetime import datetime
from typing import List

from app.db.models import Activity, UserPreferences
from app.planner.activities.base import BaseActivity


class WeatherStrategy(ABC):
    """Strategy interface used by DayPlanner to choose activities."""

    @abstractmethod
    def base_activities(self) -> List[BaseActivity]:
        raise NotImplementedError

    def get_activities(self, user_preferences: UserPreferences) -> List[Activity]:
        candidates = [activity.to_activity() for activity in self.base_activities()]
        filtered = [a for a in candidates if a.type not in user_preferences.avoid_types]

        now = datetime.now()
        is_weekend = now.weekday() >= 5
        working_hours = range(user_preferences.working_hours_start, user_preferences.working_hours_end + 1)

        for activity in filtered:
            # Коригуємо пріоритети відповідно до вподобань та контексту часу
            if activity.type in user_preferences.preferred_types:
                activity.priority += 1
            if user_preferences.prefers_outdoor and activity.type == "outdoor":
                activity.priority += 1
            if not user_preferences.prefers_outdoor and activity.type == "outdoor":
                activity.priority -= 1
            if is_weekend and user_preferences.weekend_mode and activity.type in {"leisure", "outdoor"}:
                activity.priority += 1
            if is_weekend and not user_preferences.weekend_mode and activity.type == "productive":
                activity.priority -= 1
            if now.hour in working_hours and activity.type in {"leisure", "sport"}:
                activity.priority -= 1

        filtered = [a for a in filtered if a.priority > 0]
        filtered.sort(key=lambda a: a.priority, reverse=True)

        if not filtered:
            return [Activity(name="Read a book", type="productive", priority=1)]
        return filtered
