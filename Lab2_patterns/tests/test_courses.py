
from scheduling.courses import ProgrammingCourseFactory, DatabasesCourseFactory
from scheduling.teachers import Lecturer, Assistant, ExternalMentor

mentor = ExternalMentor("Industry Expert")
lec = Lecturer("Dr. Oleh Sinkevych")
asst = Assistant("Dr. Mariia Petrenko")

def test_abstract_factory_products():
    prog = ProgrammingCourseFactory()
    lec_s = prog.create_lecture(time="Wed 15:05", room="129", teacher=lec)
    prac_s = prog.create_practical(time="Mon 13:30", room="#3", teacher=asst)
    cw = prog.create_coursework(supervisor=mentor)

    assert lec_s.course == "Programming"
    assert prac_s.course == "Programming"
    assert "Programming" in cw.title

    db = DatabasesCourseFactory()
    cw2 = db.create_coursework(supervisor=mentor)
    assert "Databases" in cw2.title
