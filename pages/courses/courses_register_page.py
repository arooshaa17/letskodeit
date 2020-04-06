import logging
import time

import utilities.custom_logger as cl
from base.base_page import BasePage


class CourseRegisterPage(BasePage):
    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # Locators #

    _search_box = "//input[@id='search-courses']"
    _course = "//div[@title='JavaScript for beginners']"
    _search_button = "//button[@id='search-course-button']"
    _enroll_button = "//button[@id='enroll-button-top']"
    _cc_num = "//span[@class='InputContainer']//input[@name='cardnumber']"
    _cc_exp = "//span[@class='InputContainer']//input[@name='exp-date']"
    _cc_cvc = "//span[@class='InputContainer']//input[@name='cvc']"
    _submit_enroll = "//button[@id='confirm-purchase']"

    # Element Interactions #

    def enterCourseName(self, name):
        self.enterData(name, self._search_box)
        self.elementClick(self._search_button)

    def selectCourseToEnroll(self):
        self.elementClick(self._course)

    def clickEnrollButton(self):
        self.elementClick(self._enroll_button)

    def enterCardNum(self, num):
        self.switchFrame(0)
        self.enterData(num, self._cc_num)

    def enterCardExp(self, exp):
        self.switchFrame(1)
        self.enterData(exp, self._cc_exp)

    def enterCardCVV(self, cvv):
        self.switchFrame(2)
        self.enterData(cvv, self._cc_cvc)

    def enterCreditCardInformation(self, num, exp, cvv):
        self.enterCardNum(num)
        self.enterCardExp(exp)
        self.enterCardCVV(cvv)

    def clickEnrollSubmitButton(self):
        self.elementClick(self._submit_enroll)

    def enrollCourse(self, num, exp, cvv):
        self.clickEnrollButton()
        self.scrollPage(650)
        self.enterCreditCardInformation(num, exp, cvv)
        self.scrollPage(200)
        time.sleep(3)
        self.clickEnrollSubmitButton()

    # def verifyEnrollFailed(self):
    #     result = self.isElementDisplayed(self._submit_enroll)
    #     return result

    def verifyEnrollFailed(self):
        result = self.elementIsEnabled(self._submit_enroll)
        return not result
