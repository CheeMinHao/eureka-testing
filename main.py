from selenium import webdriver
import time

from selenium.webdriver.common.by import By

import os
from dotenv import load_dotenv

load_dotenv()

# Configure drive
driver = webdriver.Chrome("C:/WebDriver/bin/chromedriver")

# Open Web Browser
driver.implicitly_wait(30)
driver.set_page_load_timeout(50)
driver.get("https://eureka-monash.com")

# Conifgure main page (to handle redirection of windows)
main_page = driver.current_window_handle

# Logging in from Home Page
driver.find_element_by_id("top-nav__name").click()
driver.find_element_by_tag_name("button").click()

for handle in driver.window_handles:
    if handle != main_page:
        login_page = handle

# Switch to Auth Page
driver.switch_to.window(login_page)

# Input Credentials & Proceeding
driver.find_element_by_css_selector("input[type=email]").send_keys(os.getenv("USER_NAME"))
driver.find_element_by_class_name("VfPpkd-LgbsSe").click()

driver.find_element_by_name("username").send_keys(os.getenv("USER_NAME"))
driver.find_element_by_name("password").send_keys(os.getenv("PASSWORD"))



time.sleep(10)
driver.quit()
