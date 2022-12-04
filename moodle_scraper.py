from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

ASSIGNMENT_PATH_PREFIX = "/mod/assign/index.php"#Is it different for each moodle page?
MOODLE_URL = "https://el1.netanya.ac.il"

debug_url = ""
logged_in = False
browser = None
def start():
	global browser
	browser = webdriver.Chrome()
def login(username = "", password = ""):
	global logged_in
	global browser
	if(logged_in):return
	browser.get("https://login.netanya.ac.il/nidp/saml2/sso?id=loa2&sid=0&option=credential&sid=0")
	username_form = browser.find_element(By.ID,"Ecom_User_ID")
	username_form.send_keys(username,Keys.ENTER)
	password_button = browser.find_element(By.ID,"ldapPasswordCardClick")
	browser.implicitly_wait(10)
	time.sleep(5)
	ActionChains(browser).move_to_element(password_button).click(password_button).perform()
	password_form = browser.find_element(By.ID,"ldapPassword")
	password_form.send_keys(password,Keys.ENTER)
	logged_in = True

def get_tasks_for_course_id(course_id):
	global logged_in
	global browser
	if(not logged_in):
		print("Login First")
		return
	browser.get(MOODLE_URL + ASSIGNMENT_PATH_PREFIX +'?id='+ str(course_id))
	browser.get(MOODLE_URL + ASSIGNMENT_PATH_PREFIX +'?id='+ str(course_id))
	time.sleep(3)
	table = browser.find_element(By.TAG_NAME,"tbody")
	cells = table.find_elements(By.TAG_NAME,"td")
	assignments = []
	i = 0
	assi = []
	for cell in cells:
		assi.append(cell.text)
		if( i % 5 ==1):
			try:
				href = cell.find_element(By.XPATH, "//a")
				assi.append(href.get_attribute('href'))
			except:
				print("Failed to find href in cell #"+str(i),"(",cell.text,")","of course",course_id)
		if((i+1)%5 == 0 and assi != []):
			assignments.append(assi.copy())#! If any assignment value errors arise, change to deep copy
			assi.clear()
		i = i+1
	return assignments
#TODO implement this execption prevention mechanism
# element = WebDriverWait(browser, 10).until(
    #     	EC.presence_of_element_located((By.CLASS_NAME,class_name))
    # 		)