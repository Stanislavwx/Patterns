
from __future__ import annotations
from dataclasses import dataclass
from .timeslot import TimeSlot
from .teachers import Teacher

@dataclass(frozen=True)
class Session:
    time: TimeSlot
    room: str
    teacher: Teacher
    course: str

@dataclass(frozen=True)
class LectureSession(Session):
    def __post_init__(self):
        if not self.teacher.can_give_lecture():
            raise PermissionError(f"{self.teacher.name} cannot give lectures")

@dataclass(frozen=True)
class PracticalSession(Session):
    def __post_init__(self):
        if not self.teacher.can_lead_practical():
            raise PermissionError(f"{self.teacher.name} cannot lead practicals")
