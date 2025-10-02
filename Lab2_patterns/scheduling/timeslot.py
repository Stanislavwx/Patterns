
from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple

_DAYS = {
    "Mon": 0, "Tue": 1, "Wed": 2, "Thu": 3, "Fri": 4, "Sat": 5, "Sun": 6
}

@dataclass(frozen=True)
class TimeSlot:
    day: int           # 0..6
    start_minutes: int # minutes from 00:00
    duration: int = 90 # default 1.5h lecture

    @staticmethod
    def parse(text: str, default_duration: int = 90) -> "TimeSlot":
        """Parse strings like 'Mon 13:30' or 'Wed 15:05'."""
        day_str, hm = text.strip().split()
        if day_str not in _DAYS:
            raise ValueError(f"Unknown day '{day_str}', use Mon/Tue/.../Sun")
        h, m = hm.split(":")
        return TimeSlot(_DAYS[day_str], int(h)*60 + int(m), default_duration)

    def overlaps(self, other: "TimeSlot") -> bool:
        if self.day != other.day:
            return False
        end = self.start_minutes + self.duration
        o_end = other.start_minutes + other.duration
        return not (end <= other.start_minutes or o_end <= self.start_minutes)

    def __str__(self) -> str:
        day = list(_DAYS.keys())[self.day]
        h = self.start_minutes // 60
        m = self.start_minutes % 60
        return f"{day} {h:02d}:{m:02d}"
