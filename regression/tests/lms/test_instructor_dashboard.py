"""
End to end tests for Instructor Dashboard.
"""
import os
from time import sleep

from unittest import skipIf, skip
from bok_choy.web_app_test import WebAppTest
from bok_choy.browser import browser

from regression.pages.lms import LMS_BASE_URL, LMS_STAGE_BASE_URL
from regression.pages.lms.dashboard_lms import DashboardPageExtended
from regression.pages.lms.instructor_dashboard import (
    InstructorDashboardPageExtended
)
from regression.pages.lms.course_page_lms import CourseInfoPageExtended
from regression.pages.lms.course_about_page import CourseAboutPageExtended
from regression.pages.lms.register_page import RegisterPageExtended
from regression.pages.lms.courseware_page import CoursewarePageExtended
from regression.pages.lms.activate_account import ActivateAccountExtended
from regression.pages.lms.login_lms import LmsLogin
from regression.tests.helpers.utils import (
    get_course_info, get_course_display_name
)
from regression.tests.helpers.api_clients import LmsLoginApi
from regression.pages.lms.utils import get_course_key

import regression.tests.helpers.utils as Helper
from regression.tests.helpers.api_clients import GuerrillaMailApi


class AnalyticsTest(WebAppTest):
    """
    Regression tests on Analytics on Instructor Dashboard
    """

    def setUp(self):
        super(AnalyticsTest, self).setUp()

        login_api = LmsLoginApi()
        login_api.authenticate(self.browser)

        course_info = get_course_info()
        self.dashboard_page = DashboardPageExtended(self.browser)
        self.instructor_dashboard = InstructorDashboardPageExtended(
            self.browser,
            get_course_key(course_info)
        )
        self.course_page = CourseInfoPageExtended(
            self.browser,
            get_course_key(course_info)
        )
        
        self.course_info = get_course_key(get_course_info())
        self.course_about_page = CourseAboutPageExtended(self.browser, self.course_info)
        self.course_about_page.visit()
        self.course_about_page.enroll_if_unenroll()

        self.dashboard_page.visit()
        self.dashboard_page.select_course(get_course_display_name())
        self.course_page.wait_for_page()
        self.instructor_dashboard.visit()

    @skipIf(
        LMS_BASE_URL != LMS_STAGE_BASE_URL,
        "Url can't be tested on sandbox"
    )  # LT-61
    def test_analytics_link(self):
        """
        Verifies that edX Insights link is clicked and displayed
        """
        self.instructor_dashboard.click_analytics_tab()
        self.assertEquals(
            self.instructor_dashboard.get_insights_title_text(),
            'INSIGHTS'
        )

    def test_instructor_dashboard(self):
        """
        Verifies that instructor can send bulk emails
        """
        bulk_email_page = self.instructor_dashboard.select_bulk_email()
        bulk_email_page.is_browser_on_page()
        bulk_email_page.send_message(['myself'])
        bulk_email_page.verify_message_queued_successfully()

    def test_task_status(self):
        """
        Verifies status for the tasks for user
        """
        self.instructor_dashboard.q(css='[data-section="student_admin"]').first.click()

        username = "staff"
        location = "block-v1:edX+DemoX+Demo_Course+type@problem+block@9cee77a606ea4c1aa5440e0ea5d0f618"
        self.instructor_dashboard.q(css='[name="student-select-grade"]').fill(username)
        self.instructor_dashboard.q(css='[name="problem-select-single"]').fill(location)
        self.instructor_dashboard.q(css='[name="rescore-problem-if-higher-single"]').first.click()
        self.instructor_dashboard.q(css='[name="task-history-single"]').first.click()

        self.instructor_dashboard.wait_for_element_visibility('div.task-history-single-table', 'description')

        self.assertIn(
            "rescore_problem_if_higher",
            self.instructor_dashboard.q(css='div.slick-cell.l0.r0')[0].text
        )

        self.assertIn(
            location,
            self.instructor_dashboard.q(css='div.slick-cell.l1.r1')[0].text
        )

        self.assertIn(
            username,
            self.instructor_dashboard.q(css='div.slick-cell.l3.r3')[0].text
        )

#TODO:need to fix guerrillamail
class StudentAdminTest(WebAppTest):
    DEMO_COURSE_USER = os.environ.get('USER_LOGIN_EMAIL')
    DEMO_COURSE_PASSWORD = os.environ.get('USER_LOGIN_PASSWORD')
    LMS_BASE_URL = os.environ.get('LMS_BASE_URL')

    def setUp(self):
        super(StudentAdminTest, self).setUp()
        course_info = get_course_info()
        self.login_page = LmsLogin(self.browser)

        self.course_about_page = CourseAboutPageExtended(
            self.browser,
            get_course_key(course_info)
        )
        self.courseware_page = CoursewarePageExtended(
            self.browser,
            get_course_key(course_info)
        )
        self.dashboard_page = DashboardPageExtended(self.browser)
        self.instructor_dashboard = InstructorDashboardPageExtended(
            self.browser,
            get_course_key(course_info)
        )
        self.course_page = CourseInfoPageExtended(
            self.browser,
            get_course_key(course_info)
        )

    # @classmethod
    # def setUpClass(cls):
    #     cls.browser = browser()
    #     cls.user_registration = RegisterPageExtended(cls.browser)
    #     cls.dashboard_page = DashboardPageExtended(cls.browser)
    #     cls.user_registration.visit()
    #     cls.creds = Helper.get_random_credentials()

    #     cls.user_registration.is_browser_on_page()

    #     GuerillaMail = GuerrillaMailApi(cls.creds[0])
    #     cls.generate_email = GuerillaMail.user_email
    #     cls.user_pass = '123456'
    #     cls.user_registration.register_user(
    #         email=cls.generate_email,
    #         password=cls.user_pass,
    #         country='US',
    #         username=cls.creds[0],
    #         full_name='name',
    #         terms_of_service=True,
    #     )
    #     cls.dashboard_page.is_browser_on_page()

    #     main_window = cls.browser.current_window_handle
    #     # Get activation link from email
    #     activation_url = GuerrillaMailApi(cls.creds[0]).get_url_from_email(
    #         'activate'
    #     )
    #     #if link in email isnt valid, this method will make it valid
    #     if activation_url.count('https') > 1:
    #         updated_link = activation_url.split('"')
    #         valid_link = updated_link[0]
    #     else:
    #         valid_link = activation_url

    #     # Open a new window and go to activation link in this window
    #     cls.browser.execute_script("window.open('');")
    #     cls.browser.switch_to.window(cls.browser.window_handles[-1])
    #     account_activate_page = ActivateAccountExtended(cls.browser, valid_link)
    #     account_activate_page.visit()
    #     # Verify that activation is complete
    #     cls.browser.close()
    #     # Switch back to original window and refresh the page
    #     cls.browser.switch_to.window(main_window)
    #     cls.browser.close()

    @skip(
        'need to fix guerrillamail'
    )
    def test_delete_lerner_state(self):
        """
        Verifies status for the tasks for user
        """

        self.login_page.visit()
        self.login_page.login(self.generate_email, self.user_pass)

        self.course_about_page.visit()
        self.course_about_page.enroll_button.click()
        self.dashboard_page.wait_for_page()
        self.courseware_page.visit()
        self.courseware_page.q(css='#tab_6').first.click()
        self.courseware_page.q(css='#input_932e6f2ce8274072a355a94560216d1a_2_1_choice_2').first.click()
        self.courseware_page.q(css='[aria-describedby="submission_feedback_932e6f2ce8274072a355a94560216d1a"]').first.click()

        login_api = LmsLoginApi()
        login_api.authenticate(self.browser)
        self.dashboard_page.visit()
        self.dashboard_page.select_course(get_course_display_name())
        self.course_page.wait_for_page()
        self.instructor_dashboard.visit()

        self.instructor_dashboard.q(css='[data-section="student_admin"]').first.click()

        location = "block-v1:edX+DemoX+Demo_Course+type@problem+block@932e6f2ce8274072a355a94560216d1a"
        self.instructor_dashboard.q(css='[name="student-select-grade"]').fill(self.creds[0])
        self.instructor_dashboard.q(css='[name="problem-select-single"]').fill(location)
        self.instructor_dashboard.q(css='[name="rescore-problem-single"]').first.click()
        sleep(1)
        self.instructor_dashboard.q(css='[name="task-history-single"]').first.click()

        self.instructor_dashboard.wait_for_element_visibility('div.task-history-single-table', 'description')

        self.assertIn(
            location,
            self.instructor_dashboard.q(css='div.slick-cell.l1.r1')[0].text
        )

        self.assertEquals(
            "Complete",
            self.instructor_dashboard.q(css='div.slick-cell.l7.r7')[0].text
        )

        self.assertIn(
            self.creds[0],
            self.instructor_dashboard.q(css='div.slick-cell.l8.r8')[0].text
        )

        self.instructor_dashboard.q(css='[name="delete-state-single"]').first.click()
        sleep(1)
        alert = self.browser.switch_to_alert()
        alert.accept()
        sleep(1)
        self.instructor_dashboard.q(css='[name="rescore-problem-single"]').first.click()
        sleep(1)
        self.instructor_dashboard.q(css='[name="task-history-single"]').first.click()
        self.instructor_dashboard.wait_for_ajax()
        self.assertEquals(
            "Incomplete",
            self.instructor_dashboard.q(css='.slick-cell.l7.r7')[0].text
        )
