
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class Teacher:
    name: str
    def can_give_lecture(self) -> bool: return False
    def can_lead_practical(self) -> bool: return False
    def can_supervise_coursework(self) -> bool: return False

class Lecturer(Teacher):
    def can_give_lecture(self) -> bool: return True
    def can_lead_practical(self) -> bool: return False
    def can_supervise_coursework(self) -> bool: return True

class Assistant(Teacher):
    def can_give_lecture(self) -> bool: return False
    def can_lead_practical(self) -> bool: return True
    def can_supervise_coursework(self) -> bool: return True

class ExternalMentor(Teacher):
    def can_give_lecture(self) -> bool: return False
    def can_lead_practical(self) -> bool: return False
    def can_supervise_coursework(self) -> bool: return True
