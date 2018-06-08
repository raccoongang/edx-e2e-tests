"""
End to end tests for course enrollment/unenrollment.
"""

from regression.tests.helpers.api_clients import LmsLoginApi
from regression.pages.lms.dashboard_lms import DashboardPageExtended
from regression.pages.lms.course_about_page import CourseAboutPageExtended
from bok_choy.web_app_test import WebAppTest
from regression.pages.lms.utils import get_course_key
from regression.tests.helpers.utils import (
    get_course_info)


class TestCourseEnrollment(WebAppTest):
    """
    About page is opened and student is enrolled to a course
    If student was already enrolled, he goes to dashboard page,
    unenrolled from course and enroll to it again
    """

    def setUp(self):
        super(TestCourseEnrollment, self).setUp()
        self.course_info = get_course_info()
        self.course_about_page = CourseAboutPageExtended(self.browser, get_course_key(self.course_info))
        self.dashboard_page = DashboardPageExtended(self.browser)

    def test_course_enrollment(self):
        login_api = LmsLoginApi()
        login_api.authenticate(self.browser)

        self.course_about_page.visit()

        if self.course_about_page.enroll_button.text == u'Enroll' or \
            self.course_about_page.enroll_button.text == 'ENROLL IN DEMOX':
            self.course_about_page.enroll_button.click()
            self.dashboard_page.wait_for_page()
            self.dashboard_page.is_browser_on_page()
        elif self.course_about_page.enroll_button.text == u'View Course' or \
                u'YOU ARE ENROLLED IN THIS COURSE VIEW COURSE':
            self.dashboard_page.visit()
            self.dashboard_page.unenrollment(get_course_key(self.course_info))
            self.dashboard_page.wait_for_page()
            self.course_about_page.visit()
            if self.course_about_page.enroll_button.text == u'Enroll' or \
                self.course_about_page.enroll_button.text == 'ENROLL IN DEMOX':
                self.course_about_page.enroll_button.click()
                self.dashboard_page.wait_for_page()
                self.dashboard_page.is_browser_on_page()
        else:
            print(self.course_about_page.enroll_button.text)
            raise AssertionError
