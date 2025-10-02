
import pytest
from scheduling.sessions import LectureSession, PracticalSession
from scheduling.timeslot import TimeSlot
from scheduling.teachers import Lecturer, Assistant, ExternalMentor

lec = Lecturer("Lec")
asst = Assistant("Asst")
ment = ExternalMentor("Mentor")

def test_lecturer_can_give_lecture():
    s = LectureSession(time=TimeSlot.parse("Mon 09:00"), room="A", teacher=lec, course="X")
    assert s.teacher is lec

def test_external_mentor_cannot_give_lecture():
    with pytest.raises(PermissionError):
        LectureSession(time=TimeSlot.parse("Mon 09:00"), room="A", teacher=ment, course="X")

def test_assistant_can_lead_practical():
    s = PracticalSession(time=TimeSlot.parse("Mon 09:00"), room="A", teacher=asst, course="X")
    assert s.teacher is asst
