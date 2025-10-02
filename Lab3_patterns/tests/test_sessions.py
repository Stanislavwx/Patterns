
from scheduling.factories import LectureFactory, PracticalFactory
from scheduling.sessions import LectureSession, PracticalSession
from scheduling.teachers import Lecturer, Assistant

def test_lecture_factory_creates_lecture():
    factory = LectureFactory("Programming")
    teacher = Lecturer("Dr. Oleh Sinkevych")
    session = factory.create_session(time="Wed 15:05", room="129", teacher=teacher)
    assert isinstance(session, LectureSession)
    assert session.teacher == teacher
    assert session.room == "129"

def test_practical_factory_creates_practical():
    factory = PracticalFactory("Programming")
    teacher = Assistant("Dr. Mariia Petrenko")
    session = factory.create_session(time="Mon 13:30", room="#3", teacher=teacher)
    assert isinstance(session, PracticalSession)
    assert session.teacher == teacher
    assert str(session.time) == "Mon 13:30"
