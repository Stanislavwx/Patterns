
from __future__ import annotations
from .sessions import LectureSession, PracticalSession, Session
from .timeslot import TimeSlot
from .teachers import Teacher

class SessionFactory:
    def __init__(self, course_name: str):
        self.course_name = course_name

    def create_session(self, *, time: str, room: str, teacher: Teacher) -> Session:
        raise NotImplementedError

class LectureFactory(SessionFactory):
    def create_session(self, *, time: str, room: str, teacher: Teacher) -> LectureSession:
        return LectureSession(time=TimeSlot.parse(time), room=room, teacher=teacher, course=self.course_name)

class PracticalFactory(SessionFactory):
    def create_session(self, *, time: str, room: str, teacher: Teacher) -> PracticalSession:
        return PracticalSession(time=TimeSlot.parse(time), room=room, teacher=teacher, course=self.course_name)
