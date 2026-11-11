# шапка с исключениями и тд
dep_name = [
        "кафедра радиофизики и цифровых медиа технологий",
        "кафедра квантовой радиофизики и оптоэлектроники",
        "кафедра физической электроники и нанотехнологий",
        "кафедра информатики и компьютерных систем",
        "кафедра интеллектуальных систем",
        "кафедра кибербезопасности и информационных технологий",
        "кафедра системного анализа и компьютерного моделирования",
        "кафедра физики и аэрокосмических технологий",
        "кафедра высшей математики и математической физики"
    ]

specialties = [
    "радиофизика",
    "кибербезопасность",
    "прикладная информатика",
]
dep_specialty = {
    "радиофизика" : ["кафедра радиофизики и цифровых медиа технологий", 
     "кафедра квантовой радиофизики и оптоэлектроники",
     "кафедра физической электроники и нанотехнологий",
     "кафедра информатики и компьютерных систем",
     "кафедра физики и аэрокосмических технологий"], 
    "интеллектуальная электроника" : ["кафедра информатики и компьютерных систем"],
    "кибербезопасность" : ["кафедра кибербезопасности и информационных технологий"],
    "прикладная информатика" : ["кафедра интеллектуальных систем",
      "кафедра системного анализа и компьютерного моделирования"] }
# дисциплины допишу
curriculum = {
    "радиофизика": {
        "кафедра высшей математики и математической физики" : [("математический анализ", 1), ("ДУ", 3)],
        "кафедра информатики и компьютерных систем" : [("программирование на c++", 1), ("программирование на c++", 2)],
        "кафедра системного анализа и компьютерного моделирования" : [("базы данных", 4)],
    },
    "прикладная информатика": {
        "кафедра информатики и компьютерных систем" : [("программирование на c++", 1), ("программирование на c++", 2)],
        "кафедра интеллектуальных систем": [("программирование на Python", 3)],
        "кафедра высшей математики и математической физики" : [("ДУ", 3)],
        "кафедра системного анализа и компьютерного моделирования" : [("ТВиМС", 3), ("Имитационное моделирование", 4), 
        ("Дискретно-событийное моделирование", 6)]
    },
    "кибербезопасность" : {
        "кафедра информатики и компьютерных систем" : [("программирование на c++", 1), ("программирование на c++", 2)],
        "кафедра высшей математики и математической физики" : [("ДУ", 3)],
        "кафедра системного анализа и компьютерного моделирования" : [("базы данных", 4)]
        }
}
class Discipline:
    def __init__(self, name, semester):
        self.name = name
        self.semester = semester

class Department:
    def __init__(self, name):
        self.name = name
        self.disciplines = {}
    def add_discipline(self, discipline):
        self.disciplines[discipline.name] = discipline

class Specialty:
    def __init__(self, name):
        self.name = name
        self.departments = {}

class Student:
    def __init__(self, student_id, name, specialty):
        self.student_id = student_id
        self.name = name
        self.specialty = specialty
        self.semester = 1
        self.major_disciplines = {}

class Faculty:
    def __init__(self, name):
        self.name = name
        self.specialties = {}
        self.students = {}
        self.next_id = 2521000
        self.departments = {}

    def add_specialty(self, name):
        self.specialties[name] = Specialty(name)
# enroll_student remake
    def enroll_student(self, name, specialty_name):
        if specialty_name == self.specialties:
            specialty = self.specialties[specialty_name]
            self.next_id = name.student_id
            Student(self.next_id, name, specialty)
            self.next_id += 1
            self.students[student_id] = student
        return student_id

    def expel_student(self, student_id):
        self.get_student(student_id)
        del self.students[student_id]

    def add_discipline_to_student(self, student_id, discipline_name):
        self.get_student(student_id)
        if discipline_name in student.major_disciplines:
            AlreadyEnrolledError()
        else:
           if self.check_discipline_available(student, discipline_name) == True:
               student.major_disciplines[discipline_name] = None
            else:
               DisciplineNotAvailableError

    def remove_discipline_from_student(self, student_id, discipline_name):
        self.get_student(student_id)
        if discipline_name not in student.major_disciplines:
            NotEnrolledError
        else:
            del student.major_disciplines(discipline_name)

    def set_grade(self, student_id, discipline_name, grade):
               

    def get_student(self, student_id):
        if student_id[self.students]:
            return Student.self
       # else StudentFoundError()

    def check_discipline_available(self, student, discipline_name):
    