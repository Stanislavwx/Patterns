from datetime import date
from typing import Dict, List, Optional

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.logger import get_logger
from app.db.models import Activity, Plan, UserPreferences, WeatherData
from app.planner.strategies import (
    CloudyWeatherStrategy,
    RainyWeatherStrategy,
    SnowyWeatherStrategy,
    SunnyWeatherStrategy,
    WeatherStrategy,
)

logger = get_logger(__name__)


class DayPlanner:
    """Observer that rebuilds plans when weather updates arrive."""

    def __init__(self, db: AsyncIOMotorDatabase, default_city: str):
        self.db = db
        self.default_city = default_city
        self.strategy_map: Dict[str, WeatherStrategy] = {
            "sunny": SunnyWeatherStrategy(),
            "clear": SunnyWeatherStrategy(),
            "rain": RainyWeatherStrategy(),
            "drizzle": RainyWeatherStrategy(),
            "thunderstorm": RainyWeatherStrategy(),
            "cloudy": CloudyWeatherStrategy(),
            "clouds": CloudyWeatherStrategy(),
            "snow": SnowyWeatherStrategy(),
        }

    async def get_preferences(self, user_id: str) -> UserPreferences:
        preferences_collection = self.db["preferences"]
        doc = await preferences_collection.find_one({"user_id": user_id})
        if doc:
            return UserPreferences(**doc["preferences"])

        # Якщо уподобання ще не задані — створюємо дефолтні
        prefs = UserPreferences()
        await preferences_collection.insert_one({"user_id": user_id, "preferences": prefs.model_dump()})
        return prefs

    async def set_preferences(self, user_id: str, preferences: UserPreferences) -> UserPreferences:
        preferences_collection = self.db["preferences"]
        await preferences_collection.update_one(
            {"user_id": user_id},
            {"$set": {"preferences": preferences.model_dump()}},
            upsert=True,
        )
        logger.info("Updated preferences for user %s", user_id)
        return preferences

    def _resolve_strategy(self, condition: str) -> WeatherStrategy:
        # Підбираємо стратегію під тип погоди (fallback — хмарно)
        key = condition.lower()
        if key in self.strategy_map:
            return self.strategy_map[key]
        for prefix, strategy in self.strategy_map.items():
            if key.startswith(prefix):
                return strategy
        return CloudyWeatherStrategy()

    async def update(self, weather: WeatherData, user_id: str = "default") -> Plan:
        preferences = await self.get_preferences(user_id)
        strategy = self._resolve_strategy(weather.condition)
        activities = strategy.get_activities(preferences)

        plan = Plan(
            date=date.today(),
            location=self.default_city,
            weather=weather,
            activities=activities,
            user_id=user_id,
        )
        await self.save_plan(plan)
        logger.info("Plan updated for %s under %s conditions", user_id, weather.condition)
        return plan

    async def save_plan(self, plan: Plan) -> None:
        plans = self.db["plans"]
        payload = plan.model_dump(by_alias=True)
        payload["date"] = plan.date.isoformat()
        # Avoid inserting explicit null _id which causes duplicate key errors
        if payload.get("_id") is None:
            payload.pop("_id", None)
        await plans.insert_one(payload)

    async def get_latest_plan(self, user_id: str = "default") -> Optional[Plan]:
        plans = self.db["plans"]
        doc = await plans.find_one({"user_id": user_id}, sort=[("weather.fetched_at", -1), ("date", -1)])
        if not doc:
            return None
        doc["_id"] = str(doc["_id"])
        return Plan.model_validate(doc)

    async def list_plans(self, user_id: str = "default", limit: int = 10) -> List[Plan]:
        cursor = (
            self.db["plans"]
            .find({"user_id": user_id})
            .sort([("weather.fetched_at", -1), ("date", -1)])
            .limit(limit)
        )
        plans: List[Plan] = []
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            plans.append(Plan.model_validate(doc))
        return plans
