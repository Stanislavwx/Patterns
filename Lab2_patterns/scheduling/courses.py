
from __future__ import annotations
from dataclasses import dataclass
from .factories import LectureFactory, PracticalFactory
from .courseworks import CourseWork, OnlineSubmission, GitHubSubmission, OralDefense
from .teachers import Teacher
from .sessions import LectureSession, PracticalSession

@dataclass
class CourseFactory:
    course_name: str

    def create_lecture(self, *, time: str, room: str, teacher: Teacher) -> LectureSession:
        return LectureFactory(self.course_name).create_session(time=time, room=room, teacher=teacher)

    def create_practical(self, *, time: str, room: str, teacher: Teacher) -> PracticalSession:
        return PracticalFactory(self.course_name).create_session(time=time, room=room, teacher=teacher)

    def create_coursework(self, *, supervisor: Teacher) -> CourseWork:
        raise NotImplementedError

class ProgrammingCourseFactory(CourseFactory):
    def __init__(self): super().__init__("Programming")
    def create_coursework(self, *, supervisor: Teacher) -> CourseWork:
        return GitHubSubmission(supervisor=supervisor, title=f"{self.course_name} Project")

class DatabasesCourseFactory(CourseFactory):
    def __init__(self): super().__init__("Databases")
    def create_coursework(self, *, supervisor: Teacher) -> CourseWork:
        return OnlineSubmission(supervisor=supervisor, title=f"{self.course_name} Lab Report")

class MathCourseFactory(CourseFactory):
    def __init__(self): super().__init__("Math")
    def create_coursework(self, *, supervisor: Teacher) -> CourseWork:
        return OralDefense(supervisor=supervisor, title=f"{self.course_name} Oral Exam")
