from fake_useragent import UserAgent
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import getpass

PATH_TO_DRIVER = "./chromedriver.exe"  # change this to your web driver

ua = UserAgent(fallback='google chrome')
agent = ua.random

options = Options()
options.headless = True
options.add_argument('lang=en_US.UTF-8')
options.add_argument('user-agent="%s"' % agent)

driver = webdriver.Chrome(PATH_TO_DRIVER, chrome_options=options)  # I am using chrome

driver.get("https://eclass.srv.ualberta.ca/my/")

login = False
username = None
password = None

while not login:
    try:
        if "https://eclass.srv.ualberta.ca" in driver.current_url:
            raise TimeoutException
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.ID, "username")))
        username = driver.find_element_by_id("username")
        password = driver.find_element_by_id("user_pass")
    except TimeoutException:
        if "https://eclass.srv.ualberta.ca" in driver.current_url:
            login = True
            break
        else:
            print("Fatal Error! Check your network connection or the program may have been outdated.")
            driver.close()
            exit(1)

    username.clear()
    password.clear()
    username.send_keys(input("CCID: "))
    password.send_keys(getpass.getpass('Password: '))

    parts = driver.find_elements_by_css_selector("input")
    for part in parts:
        if part.get_attribute("value") == "Login":
            part.click()
    errors = driver.find_elements_by_class_name("error")
    if len(errors):
        print("Error(s) occurred!")
        for error in errors:
            print(error.text)
    else:
        login = True

try:
    WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.ID, "course_list")))
except TimeoutException:
    print("No course list")
    driver.close()
    exit(1)

name_div = driver.find_element_by_class_name("page-header-headings")
name = name_div.find_element_by_tag_name("h1")
print(name.text)

course_list = driver.find_element_by_id("course_list")
current_course_list = course_list.find_elements_by_css_selector(".box.coursebox.currentcourse")
full_course_list = course_list.find_elements_by_css_selector(".box.coursebox")
# for current_course in current_course_list:
#     course = current_course.find_element_by_tag_name("a")
#     title = course.get_attribute("title")
#     link = course.get_attribute("href")
#     print(title, link)
for current_course in full_course_list:
    course = current_course.find_element_by_tag_name("a")
    title = course.get_attribute("title")
    link = course.get_attribute("href")
    print(title, link)

driver.close()
