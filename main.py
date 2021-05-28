from selenium import webdriver
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os
from dotenv import load_dotenv

import pyotp
import unittest

load_dotenv()

class EurekaLoginTest(unittest.TestCase):

    def setUp(self):
        # Configure drive
        self.driver = webdriver.Chrome("C:/WebDriver/bin/chromedriver")
        # Open Web Browser
        self.driver.implicitly_wait(30)
        self.driver.set_page_load_timeout(50)
        self.driver.get("https://eureka-monash.com")
        self.wait = WebDriverWait(driver,10)

    def test_login(self):

        # Conifgure main page (to handle redirection of windows)
        main_page = self.driver.current_window_handle

        # Logging in from Home Page
        self.driver.find_element_by_id("top-nav__name").click()
        self.driver.find_element_by_tag_name("button").click()

        for handle in self.driver.window_handles:
            if handle != main_page:
                login_page = handle

        # Switch to Auth Page
        self.driver.switch_to.window(login_page)

        # Input Credentials & Proceeding
        self.driver.find_element_by_css_selector("input[type=email]").send_keys(os.getenv("USER_NAME"))
        self.driver.find_element_by_class_name("VfPpkd-LgbsSe").click()

        # At Monash page, input user name and password
        self.driver.find_element_by_name("username").send_keys(os.getenv("USER_NAME"))
        self.driver.find_element_by_name("password").send_keys(os.getenv("PASSWORD"))
        self.driver.find_element_by_id("okta-signin-submit").click()

        totp = pyotp.TOTP(os.getenv("SECRET_KEY"))

        authField = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='answer']")))
        token = totp.now()
        authField.send_keys(token)
        self.driver.find_element_by_xpath("//input[@type='submit']").click()

        time.sleep(10)
        self.driver.quit()
