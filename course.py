#implement Course class
import assignment
class Course:
	def __get_course_id_from_url(self,url):
		course_id_idx = url.index("id=") +len("id=")
		course_id = ""
		while(course_id_idx < len(url) and url[course_id_idx].isdigit()):
			course_id =course_id + url[course_id_idx]
			course_id_idx =course_id_idx +1
		course_id_int = int(course_id)
		return course_id_int
	
	def __init__(self,name:str,url:str):
		self.name = name
		self.url =url
		self.assignments = []
		self.id = self.__get_course_id_from_url(url)
	
	def get_assignments(self):
		import moodle_scraper as scraper
		assignments = []
		assignments = scraper.get_tasks_for_course_id(self.id)
		for task in assignments:
			name = task[1]
			url = task[2]
			date = task[3]
			isSubmitted = task[4] == "הוגש למתן ציון"
			grade = task[5]
			assi = 	assignment.Assignment(name,url,date,isSubmitted,grade)
			self.assignments.append(assi)
		return self.assignments
	
	def get_missing_assignments(self):
		res = []
		for task in self.assignments:
			if not task.isSubmitted:
				res.append(task)
		return res
