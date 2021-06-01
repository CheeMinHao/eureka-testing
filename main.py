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

class LoginTesting(unittest.TestCase):

    def setUp(self):
        # Configure drive
        self.driver = webdriver.Chrome("C:/WebDriver/bin/chromedriver")

    def test_login(self):

        driver = self.driver

        # Open Web Browser
        driver.implicitly_wait(30)
        driver.set_page_load_timeout(50)
        driver.get("https://eureka-monash.com")

        wait = WebDriverWait(driver,10)

        # Check if correct broswer connected (check if browser name is correct)
        self.assertIn("Eureka", driver.title, msg="wrong website" )

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


        # At Monash page, input user name and password
        driver.find_element_by_name("username").send_keys(os.getenv("USER_NAME"))
        driver.find_element_by_name("password").send_keys(os.getenv("PASSWORD"))
        driver.find_element_by_id("okta-signin-submit").click()

        totp = pyotp.TOTP(os.getenv("SECRET_KEY"))

        authField = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='answer']")))
        token = totp.now()
        authField.send_keys(token)
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@type='submit']")))
        driver.find_element_by_xpath("//input[@type='submit']").click()

        driver.find_element_by_class_name("VfPpkd-LgbsSe").click()

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
