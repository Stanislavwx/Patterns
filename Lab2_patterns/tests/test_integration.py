
from scheduling.courses import ProgrammingCourseFactory
from scheduling.groups import StudentGroup
from scheduling.teachers import Lecturer, Assistant, ExternalMentor

def test_group_enrollment_and_conflict_detection():
    course_factory = ProgrammingCourseFactory()
    lecturer = Lecturer("Dr. Oleh Sinkevych")
    assistant = Assistant("Dr. Mariia Petrenko")
    mentor = ExternalMentor("Industry Expert")

    group = StudentGroup("FeP-21")
    # Спеціально ставимо обидва на Mon 13:30, щоб зловити конфлікт
    group.enroll(course_factory,
                 lecture_time="Mon 13:30", lecture_room="129", lecture_teacher=lecturer,
                 practical_time="Mon 13:30", practical_room="#3", practical_teacher=assistant,
                 coursework_supervisor=mentor)

    conflicts = group.check_conflicts()
    assert len(conflicts) == 1
    assert conflicts[0].session_b.teacher == assistant
