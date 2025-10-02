
from scheduling.teachers import Lecturer, Assistant, ExternalMentor
from scheduling.courses import ProgrammingCourseFactory, DatabasesCourseFactory
from scheduling.groups import StudentGroup

if __name__ == "__main__":
    # Викладачі
    lec = Lecturer("Dr. Oleh Sinkevych")
    asst = Assistant("Dr. Mariia Petrenko")
    mentor = ExternalMentor("Industry Expert")

    # Фабрики курсів
    prog = ProgrammingCourseFactory()
    db   = DatabasesCourseFactory()

    # Групи
    g1 = StudentGroup("FeP-23")
    g2 = StudentGroup("Fep-21")

    # Запис груп
    g1.enroll(prog,
              lecture_time="Wed 15:05", lecture_room="129", lecture_teacher=lec,
              practical_time="Mon 13:30", practical_room="#3", practical_teacher=asst,
              coursework_supervisor=mentor)

    g2.enroll(db,
              lecture_time="Mon 13:30", lecture_room="129", lecture_teacher=lec,
              practical_time="Mon 13:30", practical_room="#5", practical_teacher=asst,
              coursework_supervisor=mentor)

    # Вивід конфліктів
    for group in (g1, g2):
        conflicts = group.check_conflicts()
        print(f"Group {group.name}: {len(conflicts)} conflict(s)")
        for c in conflicts:
            print(f"  {c.session_a.course} {c.session_a.time} vs {c.session_b.course} {c.session_b.time}")
