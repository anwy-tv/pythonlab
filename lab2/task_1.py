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
        self.next_id = 2521001
        self.departments = {}

    def get_student(self, student_id):
        if student_id in self.students:
            return self.students[student_id] 
        raise StudentNotFoundError(f"студент с ID {student_id} не найден")

    def add_specialty(self, name):
        self.specialties[name] = Specialty(name)

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

def generate_student_report(faculty, student_id, filename):
    student = faculty.get_student(student_id)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"имя студента: {student.name}\n")
        f.write(f"название специальности: {student.specialty.name}\n")
        f.write(f"cеместр: {student.semester}\n")
        grades_sum = 0
        grades_count = 0

        for discipline_name, grade in student.major_disciplines.items():
            department_name = "неизвестно"
            for dep_name, department in student.specialty.departments.items():
                if discipline_name in department.disciplines:
                    department_name = dep_name
                    break
            grade_str = str(grade) if grade is not None else "не сдана"
            f.write(f"{discipline_name} | {department_name} | {grade_str}\n")
            if grade is not None:
                grades_sum += grade
                grades_count += 1

        if grades_count > 0:
            average = grades_sum / grades_count
            f.write(f"средний балл: {average:.2f}\n")
        else:
            f.write("средний балл: нет оценок\n")

def generate_discipline_report(faculty, discipline_name, filename):
    departments_list = []
    for specialty in faculty.specialties.values():
        for dep_name, department in specialty.departments.items():
            if discipline_name in department.disciplines and dep_name not in departments_list:
                departments_list.append(dep_name)
    
    students_list = []
    for student in faculty.students.values():
        if discipline_name in student.major_disciplines:
            students_list.append(student)
    
    grades_sum = 0
    grades_count = 0
    for student in students_list:
        grade = student.major_disciplines[discipline_name]
        if grade is not None:
            grades_sum += grade
            grades_count += 1
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"дисциплина: {discipline_name}\n")
        f.write(f"читающие кафедры: {', '.join(departments_list) if departments_list else 'не найдены'}\n")
        
        if grades_count > 0:
            average = grades_sum / grades_count
            f.write(f"средний балл: {average:.2f}\n")
        else:
            f.write("средний балл: нет оценок\n")
        
        f.write(f"студентов изучает: {len(students_list)}\n")
        for student in students_list:
            grade = student.major_disciplines[discipline_name]
            grade_str = str(grade) if grade is not None else "не сдана"
            f.write(f"  {student.name} (ID: {student.student_id}) — {grade_str}\n")
    
def show_menu():
    print("\nМЕНЮ\n")
    print("1. зачислить студента")
    print("2. отчислить студента")
    print("3. записать студента на дисциплину")
    print("4. удалить дисциплину у студента")
    print("5. выставить оценку")
    print("6. перевести на следующий семестр")
    print("7. сформировать ведомость по студенту")
    print("8. сформировать ведомость по дисциплине")
    print("0. выход")

faculty = init_faculty()
while True:
    show_menu()
    choice = input("выберите действие: ")
    try:
        if choice == "1":
            name = input("введите имя студента: ")
            specialty_name = input("введите название специальности: ")
            student_id = faculty.enroll_student(name, specialty_name)
            print(f"студент {name} зачислен. ID: {student_id}.")
        elif choice == "2":
            student_id = int(input("введите ID студента: "))
            faculty.expel_student(student_id)
            print("студент отчислен.")
        elif choice == "3":
            student_id = int(input("введите ID студента: "))
            discipline_name = input("введите название дисциплины: ")
            faculty.add_discipline_to_student(student_id, discipline_name)
            print(f"студент записан на дисциплину '{discipline_name}'.") 
        elif choice == "4":
            student_id = int(input("введите ID студента: "))
            discipline_name = input("введите название дисциплины: ")
            faculty.remove_discipline_from_student(student_id, discipline_name)
            print(f"дисциплина '{discipline_name}' удалена у студента.")
        elif choice == "5":
            student_id = int(input("введите ID студента: "))
            discipline_name = input("введите название дисциплины: ")
            grade = int(input("введите оценку (1-10): "))
            faculty.set_grade(student_id, discipline_name, grade)
            print(f"оценка {grade} выставлена за дисциплину '{discipline_name}'.")
        elif choice == "6":
            student_id = int(input("введите ID студента: "))
            faculty.advance_student(student_id)
            print("студент переведён на следующий семестр.")
        elif choice == "7":
            student_id = int(input("введите ID студента: "))
            filename = input("введите имя файла для сохранения: ")
            generate_student_report(faculty, student_id, filename)
            print(f"ведомость сохранена в файл '{filename}'.")   
        elif choice == "8":
            discipline_name = input("введите название дисциплины: ")
            filename = input("введите имя файла для сохранения: ")
            generate_discipline_report(faculty, discipline_name, filename)
            print(f"ведомость сохранена в файл '{filename}'.")
        elif choice == "0":
            print("выход из программы.")
            break
        else:
            print("неверный выбор. введите цифру из перечня.")

    except ValueError as e:
        if "invalid literal" in str(e) or "не удалось преобразовать" in str(e).lower():
            print("ошибка: введите корректное числовое значение для ID или оценки.")
        else:
            print(f"ошибка: {e}")
    except StudentNotFoundError as e:
        print(f"ошибка: {e}")
    except SpecialtyNotFoundError as e:
        print(f"ошибка: {e}")
    except DisciplineNotAvailableError as e:
        print(f"ошибка: {e}")
    except NotEnrolledError as e:
        print(f"ошибка: {e}")
    except InvalidGradeError as e:
        print(f"ошибка: {e}")
    except AlreadyEnrolledError as e:
        print(f"ошибка: {e}")
    except Exception as e:
        print(f"неожиданная ошибка: {e}")