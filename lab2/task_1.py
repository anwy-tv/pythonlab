class StudentNotFoundError(Exception):
    def __init__(self, message="студент не найден"):
        super().__init__(message)
class SpecialtyNotFoundError(Exception):
    def __init__(self, message="специальность не найдена"):
        super().__init__(message)

class DisciplineNotAvailableError(Exception):
    def __init__(self, message="дисциплина не найдена"):
            super().__init__(message)

class NotEnrolledError(Exception):
    def __init__(self, message="студент не записан на эту дисциплину"):
            super().__init__(message)

class InvalidGradeError(Exception):
   def __init__(self, message="оценка некорректна"):
           super().__init__(message)

class AlreadyEnrolledError(Exception):
    def __init__(self, message="студент уже записан на эту дисциплину"):
            super().__init__(message)

class StudentAlreadyExistsError(Exception):
    def __init__(self, message="студент с таким ID уже существует"):
            super().__init__(message)

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

specialties = [ "радиофизика", "кибербезопасность", "прикладная информатика" ]
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

    def get_student(self, student_id):
            if student_id in self.students:
                return self.students[student_id]
            else: 
                raise StudentNotFoundError(f"студент с ID {student_id} не найден")

    def add_specialty(self, name):
        self.specialties[name] = Specialty(name)
# enroll_student remake

    def enroll_student(self, name, specialty_name):
        if specialty_name not in self.specialties:
            raise SpecialtyNotFoundError(f"специальность '{specialty_name}' не найдена")
        specialty = self.specialties[specialty_name]
        student_id = self.next_id
        student = Student(student_id, name, specialty)
        self.next_id += 1
        self.students[student_id] = student
        return student_id

    def expel_student(self, student_id):
        self.get_student(student_id)
        del self.students[student_id]

    def add_discipline_to_student(self, student_id, discipline_name):
        student = self.get_student(student_id)
        if discipline_name in student.major_disciplines:
           raise AlreadyEnrolledError(f"студент уже записан на '{discipline_name}'")
        if self.check_discipline_available(student, discipline_name):
            student.major_disciplines[discipline_name] = None
        else:
            raise DisciplineNotAvailableError(f"дисциплина '{discipline_name}'не ведется для специальности '{student.specialty.name}'")

    def remove_discipline_from_student(self, student_id, discipline_name):
        student = self.get_student(student_id)
        if discipline_name not in student.major_disciplines:
            raise NotEnrolledError(f"студент не записан на дисциплину '{discipline_name}'")
        del student.major_disciplines[discipline_name]

    def set_grade(self, student_id, discipline_name, grade):
        student = self.get_student(student_id)
        if discipline_name not in student.major_disciplines:
            raise NotEnrolledError(f"студент не записан на дисциплину '{discipline_name}'")
            
        if not isinstance(grade, int) or grade < 1 or grade > 10:
            raise InvalidGradeError(f"оценка должна быть целым числом от 1 до 10")
        student.major_disciplines[discipline_name] = grade

    def advance_student(self, student_id):
        student = self.get_student(student_id)
        if not student.major_disciplines:
            raise ValueError("у студента нет дисциплин")
        for discipline_name, grade in student.major_disciplines.items():
                if grade is None or grade < 4:
                   raise ValueError(f"дисциплина '{discipline_name}' не сдана успешно. оценка: {grade}.")
        student.semester += 1

    def check_discipline_available(self, student, discipline_name):
        for department in student.specialty.departments.values():
            if discipline_name in department.disciplines:
               return True
        return False

def init_faculty():
    faculty = Faculty("Факультет радиофизики и компьютерных технологий")
    for specialty_name in specialties:
        faculty.add_specialty(specialty_name)
    for specialty_name, departments_list in dep_specialty.items():
        if specialty_name in faculty.specialties:
            specialty = faculty.specialties[specialty_name]
            for department_name in departments_list:
                department = Department(department_name)
                specialty.departments[department_name] = department
                faculty.departments[department_name] = department

    for specialty_name, curriculum_data in curriculum.items():
        if specialty_name in faculty.specialties:
            specialty = faculty.specialties[specialty_name]
            for department_name, discipline_list in curriculum_data.items():
                if department_name in specialty.departments:
                    department = specialty.departments[department_name]
                    for discipline_name, semester in discipline_list:
                        discipline = Discipline(discipline_name, semester)
                        department.add_discipline(discipline)
    return faculty