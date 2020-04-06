from base.selenium_driver import SeleniumDriver
import utilities.custom_logger as cl
from selenium.webdriver.support.ui import WebDriverWait
import logging
import time


class LoginPage(SeleniumDriver):
    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # Locators
    _login_link = "Login"
    _email_field = "user_email"
    _password_field = "user_password"
    _login_button = "commit"

    def clickLoginLink(self):
        self.elementClick(self._login_link, "link")

    def enterEmail(self, email):
        self.enterData(email, self._email_field, "id")

    def enterPassword(self, password):
        self.enterData(password, self._password_field, "id")

    def clickLoginButton(self):
        self.elementClick(self._login_button, "name")

    def login(self, email, password):
        self.clickLoginLink()
        time.sleep(5)
        self.enterEmail(email)
        self.enterPassword(password)
        self.clickLoginButton()
        time.sleep(5)
