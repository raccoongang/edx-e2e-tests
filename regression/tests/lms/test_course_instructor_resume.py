"""
 Course resume test flow by staff
"""
import os
from time import sleep

from bok_choy.web_app_test import WebAppTest

from regression.tests.helpers.utils import (
    get_course_info)
from regression.pages.lms.utils import get_course_key
from regression.pages.lms.login_lms import LmsLogin
from regression.pages.lms.dashboard_lms import DashboardPageExtended
from regression.pages.lms.courses import Courses
from regression.pages.lms.course_about_page import CourseAboutPageExtended
from regression.pages.lms.course_page_lms import CourseInfoPageExtended


class StaffCourseInstructorResume(WebAppTest):
    """
    Test flow:
     - Login as a staff
     - Go to course info and enroll
     - Course /info View as a Learner
     - Instructor tab is absent
     - Click on the Resume course button
     - /courseware is opened
     - Unenroll from course
    """

    DEMO_COURSE_USER = os.environ.get('USER_LOGIN_EMAIL')
    DEMO_COURSE_PASSWORD = os.environ.get('USER_LOGIN_PASSWORD')

    def setUp(self):
        """
        Initialize the page object
        """
        super(StaffCourseInstructorResume, self).setUp()
        self.login_page = LmsLogin(self.browser)
        self.dashboard_ext = DashboardPageExtended(self.browser)
        self.courses_page = Courses(self.browser)

        self.course_data = get_course_info()
        self.course_info = get_course_key(self.course_data)
        self.course_about_page_ext = CourseAboutPageExtended(self.browser, self.course_info)

    def test_flow(self):
        """
        Staff->Course->Instructor->Resume
        """
        # Login
        self.login_page.visit()
        self.login_page.login(self.DEMO_COURSE_USER, self.DEMO_COURSE_PASSWORD)
        self.assertEqual(
            self.login_page.q(
                css='.wrapper-header-courses .header-courses').text[0].lower(),
            'my courses',
            msg='User not logged in as expected.')

        # Open About page and enroll to the course
        course_about_page = CourseAboutPageExtended(self.browser, self.course_info)
        course_about_page.visit()

        # enroll
        sleep(2)
        course_about_page.register()
        self.dashboard_ext.visit()
        self.dashboard_ext.wait_for_page()

        # select course
        self.dashboard_ext.select_course_by_id(self.course_info)
        nav_tab_page = CourseInfoPageExtended(self.browser, self.course_info)
        nav_tab_page.go_to_tab('Course')
        nav_tab_page.wait_for_page()
        nav_tab_page.browser.refresh()

        # switch to learner preview mode
        nav_tab_page.switch_preview_mode_to('learner')

        # make sure "instructor" tab disappeared
        if nav_tab_page.has_tab('Instructor') == False:
            pass
        else:
            raise Exception('Instructor tab is present')

        #resume the course
        nav_tab_page.q(css=".action-resume-course").click()
        nav_tab_page.wait_for_page()
        sleep(1)
        self.assertIn('courseware', nav_tab_page.browser.current_url.split('/'))
        self.dashboard_ext.visit()
        self.dashboard_ext.unenrollment(self.course_info)

        course_about_page.visit()
        course_about_page.wait_for_page()
        course_about_page.is_browser_on_page()

        # Verify the Enroll button is displayed again on the /about page of course
        self.assertEquals(course_about_page.browser.find_element_by_css_selector('a.register').text.lower(),
                          ('enroll in {}'.format(self.course_data['number'])).lower())
