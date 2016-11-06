import json
import random


class Student(object):
    def __init__(self, first_name, second_name):
        self.first_name = first_name
        self.second_name = second_name
        self.scores = dict()
        self.attendances = dict()


class Diary(object):
    def __init__(self):
        self.students = list()
        self.courses = list()

    def load(self, file_name):
        """ Load diary from file with json """
        file_handler = open(file_name, 'r')
        json_object = file_handler.read()
        dictionary = json.JSONDecoder().decode(json_object)
        self.courses = list(dictionary['courses'])
        self.students = list()
        for student_dictionary in dictionary['students']:
            first_name = student_dictionary['first_name']
            second_name = student_dictionary['second_name']
            student = Student(first_name, second_name)
            student.scores = student_dictionary['scores']
            student.attendances = student_dictionary['attendances']
            self.students.append(student)

    def save(self, file_name):
        """ Save diary to file as json """
        json_object = json.dumps(self, cls=ComplexEncoder, sort_keys=True, indent=2)
        file_handler = open(file_name, 'w')
        file_handler.write(json_object)

    def add_courses(self, courses):
        Validator.validate_instance(courses, (list, tuple))
        for course in courses:
            if course not in self.courses:
                self.courses.append(course)

    def add_students(self, students):
        Validator.validate_instance(students, (list, tuple))
        for student in students:
            self.add_student(student)

    def add_student(self, student):
        try:
            Validator.validate_student(student, self.students)
        except ValueError:
            self.students.append(student)

    def add_score(self, student, course, score):
        Validator.validate_student(student, self.students)
        Validator.validate_course(course, self.courses)
        scores = student.scores.pop(course, list())
        scores.append(score)
        student.scores[course] = scores

    def add_attendance(self, student, course, attendance):
        Validator.validate_student(student, self.students)
        Validator.validate_course(course, self.courses)
        attendances = student.attendances.get(course, list())
        attendances.append(attendance)
        student.attendances[course] = attendances

    def get_total_average(self, student):
        Validator.validate_student(student, self.students)
        counter, total = 0, 0
        for v in student.scores.values():
            counter += len(v)
            total += sum(v)
        return total / counter

    def get_course_average(self, student, course):
        Validator.validate_student(student, self.students)
        Validator.validate_course(course, self.courses)
        values = student.scores[course]
        return sum(values) / len(values)

    def get_total_attendance(self, student):
        Validator.validate_student(student, self.students)
        absences, total = 0, 0
        for attendance_lis in student.attendances.values():
            total += len(attendance_lis)
            for i in attendance_lis:
                if i is False:
                    absences += 1
        return total, total-absences, absences


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        return obj.__dict__


class Validator(object):
    @staticmethod
    def validate_instance(object_to_check, tuple_of_possible_instances):
        correct_instance = False
        for instance in tuple_of_possible_instances:
            if isinstance(object_to_check, instance):
                correct_instance = True
        if not correct_instance:
            raise TypeError('Wrong instance')

    @staticmethod
    def validate_course(course, courses):
        if course not in courses:
            raise ValueError('There`s no course in list of available courses')

    @staticmethod
    def validate_student(student, students):
        Validator.validate_student_instance(student)
        if student not in students:
            raise ValueError('Student`s not in diary')

    @staticmethod
    def validate_student_instance(student):
        if not isinstance(student, Student):
            raise TypeError('It`s not Student object')


def pretty_print(print_object):
    print_object = print_object

    def print_diary():
        out_str = '\nDiary:\n'

        out_str += 'Courses:\n'
        obj_iter = print_object.courses
        for index in range(len(obj_iter)):
            obj = obj_iter[index]
            out_str += '    ' + str(index+1) + '. ' + str(obj) + '\n'

        out_str += 'Students:\n'
        obj_iter = print_object.students
        for index in range(len(obj_iter)):
            obj = obj_iter[index]
            out_str += str(index+1) + '. ' + obj.first_name + ' ' + obj.second_name
            for key in print_object.courses:
                out_str += '\n  ' + str(key)
                out_str += '\n      attendances: ' + str(obj.attendances[key])
                out_str += '\n      scores: ' + str(obj.scores[key])
            out_str += '\n'

        print out_str

    def print_student():
        print print_object.first_name, print_object.second_name

    if isinstance(print_object, Diary):
        print_diary()
    elif isinstance(print_object, Student):
        print_student()
    else:
        print print_object


def sample_diary_factory():

    def grade_possibility():
        possibility = random.randint(0, 4)
        if possibility == 0:
            out = random.randint(2, 5)
        elif possibility == 1:
            out = random.randint(3, 5)
        elif possibility == 2:
            out = 5
        else:
            out = random.randint(4, 5)
        return out

    diary = Diary()

    students = list()
    students.append(Student("Michal", "Kuklewski"))
    students.append(Student("Krzysztof", "Jamrog"))
    students.append(Student("Artur", "Rog"))
    students.append(Student("Szymon", "Kubasiak"))

    courses = ("Matematyka", "Fizyka", "Informatyka", "Angielski")
    diary.add_courses(courses)

    for student in students:
        diary.add_student(student)
        for i in range(1, 10):
            for c in courses:
                attendance = random.randint(0, 6)
                attendance = False if attendance == 0 else True
                score = grade_possibility()
                diary.add_attendance(student, c, attendance)
                diary.add_score(student, c, float(score))
    return diary
