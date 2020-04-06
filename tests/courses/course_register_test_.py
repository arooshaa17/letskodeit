import unittest
import pytest
from pages.courses.courses_register_page import CourseRegisterPage
from pages.home.login_page import LoginPage


@pytest.mark.usefixtures("oneTimeSetUp", "setUp")
class CourseRegisterTest(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def classSetup(self, oneTimeSetUp):
        self.lp = LoginPage(self.driver)
        self.courses = CourseRegisterPage(self.driver)

    @pytest.mark.run(order=1)
    def test_course_enroll(self):
        self.lp.login('test@email.com', 'abcabc')
        self.courses.enterCourseName("JavaScript")
        self.courses.selectCourseToEnroll()
        self.courses.enrollCourse('1234123412341234', '11/20', '234')
        result = self.courses.verifyEnrollFailed()
        assert result == True