
class Student(object):
	
	def __init__(self, first_name, second_name):
		self.first_name = first_name
		self.second_name = second_name
		self.scores = {}
		self.attendance = {}

class Diary(object):

	def __init__(self, file_name):
		self.file_handler = open(file_name, 'w')
		self.students = []
		self.classes = {}
		self.load()
		
	def load(self):
		pass

	
	def add_student(self, student):
		self.students.add(student)

	def get_total_average(self, student):
		if student not in self.students:
			return None
		counter = 0
		total = 0
		for i in student.scores:
			counter += len(i)
			total += sum(i)
		return total / counter

	def get_course_average(self, student, course):
		
