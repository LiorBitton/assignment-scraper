from datetime import datetime
import os
import moodle_scraper as scraper
from course import Course
#TODO make a template file for config.json once its structure is finalized
COURSES_FILE = "courses.txt"
def get_input(prompt = ""):
	reset = "\033[0m"
	res = input(prompt + "\n" + "\033[35m")
	print(reset,end="")
	return res
def get_courses():
	courses = []
	while(True):#Get courses links from the user
		print("enter exit to stop")
		url=get_input("input course URL")
		if url == "exit":
			break;
		name=get_input("input course name")
		if name == "exit":
			break;
		courses.append(Course(name = name, url = url))
	return courses
def save_courses_to_file(courses):
	with open(COURSES_FILE,"w",encoding="utf-8") as f:
		for course in courses:
			f.write(course.name)
			f.write(course.url )

username = get_input("Enter Moodle username")
password = get_input("Enter Moodle password")
courses = []
if(not os.path.exists(COURSES_FILE)):
	print("First time running...")
	print("Input some courses for me to track")
	courses.extend(get_courses())
	save_courses_to_file(courses)
else:
	answer = get_input("Do you want to add a new course?y/n")
	answer_flag = False
	if answer == "y":
		answer_flag = True
		courses.extend(get_courses())
		print("courses:",courses)
	print("Loading courses...")
	with open(COURSES_FILE,'r',encoding="utf-8") as f:
		name_line = f.readline()
		url_line = f.readline()
		while(True):
			if(name_line == "" or url_line == ""): break
			courses.append(Course(name_line,url_line))
			name_line = f.readline()
			url_line = f.readline()
	if(answer_flag):
		save_courses_to_file(courses)

scraper.start()
scraper.login(username,password)
missing_tasks = []
for course in courses:
	course.get_assignments()
	missing = course.get_missing_assignments()
	missing_tasks.extend(missing)
missing_tasks.sort(key=lambda x: x.dueDate.timestamp())
for task in missing_tasks:
	print(task)