from datetime import datetime
class Assignment:
	def __init__(self,name:str,url : str,dueDate : str,isSubmitted : bool,grade : float):
		self.name = name
		self.url = url
		self.dueDate = datetime.strptime(dueDate, '%d/%m/%Y, %H:%M')
		self.isSubmitted = isSubmitted
		self.grade = grade
	def __str__(self):
		if(self.isSubmitted):
			return f'task: {self.name} is submitted the grade is {self.grade}'
		return f'task: {self.name} --> {str(self.dueDate)}'