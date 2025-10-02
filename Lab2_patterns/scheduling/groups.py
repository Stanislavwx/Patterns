
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Tuple
from .sessions import Session

@dataclass
class Conflict:
    session_a: Session
    session_b: Session

class ScheduleValidator:
    def find_conflicts(self, sessions: List[Session]) -> List[Conflict]:
        conflicts: List[Conflict] = []
        for i in range(len(sessions)):
            for j in range(i+1, len(sessions)):
                if sessions[i].time.overlaps(sessions[j].time):
                    conflicts.append(Conflict(sessions[i], sessions[j]))
        return conflicts

@dataclass
class StudentGroup:
    name: str
    sessions: List[Session] = field(default_factory=list)
    _validator: ScheduleValidator = field(default_factory=ScheduleValidator, init=False, repr=False)

    def add_session(self, session: Session) -> None:
        self.sessions.append(session)

    def enroll(self, factory, *, lecture_time: str, lecture_room: str, lecture_teacher,
               practical_time: str, practical_room: str, practical_teacher,
               coursework_supervisor) -> Tuple[Session, Session]:
        lecture = factory.create_lecture(time=lecture_time, room=lecture_room, teacher=lecture_teacher)
        practical = factory.create_practical(time=practical_time, room=practical_room, teacher=practical_teacher)
        self.add_session(lecture)
        self.add_session(practical)
        _ = factory.create_coursework(supervisor=coursework_supervisor)
        return lecture, practical

    def check_conflicts(self):
        return self._validator.find_conflicts(self.sessions)
