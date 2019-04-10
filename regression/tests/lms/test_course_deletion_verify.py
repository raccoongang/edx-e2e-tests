"""
Course resume test flow by staff
"""

import os
from bok_choy.web_app_test import WebAppTest

from regression.tests.helpers.utils import (get_course_info)
from regression.pages.lms.login_lms import LmsLogin
from regression.pages.lms.dashboard_lms import DashboardPageExtended
from regression.pages.lms.courses import Courses
from regression.pages.lms.utils import get_course_key
from regression.pages.lms.course_about_page import CourseAboutPageExtended

import uuid
from regression.pages.studio.login_studio import StudioLogin
from regression.pages.studio.course_autoauth_page import AutoAuthPageExtended
from regression.pages.studio.studio_home import DashboardPageExtended as DashboardPageStudio


# from common.test.acceptance.tests.studio.test_studio_course_create import


class StaffCourseDeleteVerification(WebAppTest):
    """
    Test flow:
    - Login as a staff
    - Go to sysadmin tab
    - Go to course tab
    - Fill up the course ID(dir) with valid data
    - Click delete course from the site
    - The course is deleted
    """

    DEMO_COURSE_USER = os.environ.get('USER_LOGIN_EMAIL')
    DEMO_COURSE_PASSWORD = os.environ.get('USER_LOGIN_PASSWORD')

    def setUp(self):
        """
        Initialize the page object
        """

        super(StaffCourseDeleteVerification, self).setUp()

        self.login_page_studio = StudioLogin(self.browser)
        self.auth_page = AutoAuthPageExtended(self.browser, staff=True)
        self.dashboard_page = DashboardPageStudio(self.browser)
        self.course_name = "New Course Name"
        self.course_org = "orgX"
        self.course_number = str(uuid.uuid4().get_hex().upper()[0:6])
        self.course_run = "2015_T2"
        self.course_id = 'course-v1:{}+{}+{}'.format(self.course_org, self.course_number, self.course_run)

        self.login_page_studio.visit()
        self.login_page_studio.login(self.DEMO_COURSE_USER, self.DEMO_COURSE_PASSWORD)
        self.dashboard_page.visit()
        self.dashboard_page.click_new_course_button()
        self.assertTrue(self.dashboard_page.is_new_course_form_visible())
        self.dashboard_page.fill_new_course_form(
            self.course_name, self.course_org, self.course_number, self.course_run
        )
        self.assertTrue(self.dashboard_page.is_new_course_form_valid())
        self.dashboard_page.submit_new_course_form()

        self.login_page = LmsLogin(self.browser)
        self.dashboard_ext = DashboardPageExtended(self.browser)
        self.courses_page = Courses(self.browser)

        self.course_data = get_course_info()
        self.course_info = get_course_key(self.course_data)
        self.course_about_page_ext = CourseAboutPageExtended(self.browser, self.course_info)

    def test_flow(self):
        """
        Staff->Course->Delete
        """
        # login

        self.login_page.visit()
        self.login_page.login(self.DEMO_COURSE_USER, self.DEMO_COURSE_PASSWORD)
        self.assertEqual(
            self.login_page.q(
                css='.wrapper-header-courses .header-courses').text[0].lower(),
            'my courses',
            msg='User not logged in as expected'
        )

        # Open Sysadimin page by clicking on tab

        self.login_page.q(css='[href="/sysadmin/"]').click()
        self.login_page.wait_for_element_presence('[href="/sysadmin/courses"]', 'waiting the Course tab')
        self.login_page.q(css='[href="/sysadmin/courses"]').click()

        for element in self.login_page.q(css='.stat_table').text:
            if self.course_id in element:
                break
        else:
            raise Exception('Error! Search results not found')

        self.login_page.wait_for_element_presence('button[value="del_course"]', 'waiting the delete course button')

        self.login_page.q(css='input[name="course_id"]').fill(self.course_id)

        self.login_page.q(css='button[value="del_course"]').click()
        self.login_page.browser.refresh()
        self.login_page.wait_for_element_visibility(".stat_table", "Wait for the refresh page")
        # self.login_page.wait_for_invisible("")

        for element in self.login_page.q(css='.stat_table').text:
            if self.course_id in element:
                raise Exception('Error! Course not deleted!')

        assert self.login_page.q(css='font[color="red"]').text == [
            'Deleted block-v1:orgX+{0}+2015_T2+type@course+block@course = course-v1:orgX+{0}+2015_T2 (New Course Name)'.format(
                self.course_number)]
