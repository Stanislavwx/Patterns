from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class WeatherData(BaseModel):
    condition: str
    temperature: float
    description: Optional[str] = None
    fetched_at: datetime = Field(default_factory=datetime.utcnow)


class Activity(BaseModel):
    name: str
    type: str
    priority: int = 1


class UserPreferences(BaseModel):
    preferred_types: List[str] = Field(default_factory=list)
    avoid_types: List[str] = Field(default_factory=list)
    working_hours_start: int = 9
    working_hours_end: int = 17
    weekend_mode: bool = False
    prefers_outdoor: bool = True


class Plan(BaseModel):
    date: date
    location: str
    weather: WeatherData
    activities: List[Activity]
    user_id: str
    id: Optional[str] = Field(default=None, alias="_id")

    class Config:
        populate_by_name = True
