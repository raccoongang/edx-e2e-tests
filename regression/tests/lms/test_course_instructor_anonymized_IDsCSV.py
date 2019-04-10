"""
Course resume test flow by staff
"""
import os
from bok_choy.web_app_test import WebAppTest

from regression.tests.helpers.utils import (get_course_info)
from regression.pages.lms.login_lms import LmsLogin
from regression.pages.lms.dashboard_lms import DashboardPageExtended
from regression.pages.lms.instructor_dashboard import InstructorDashboardPageExtended, DataDownloadPageExtended
from regression.pages.lms.course_page_lms import CourseInfoPageExtended
from regression.pages.lms.utils import get_course_key


class StaffDownloadAnonymizedIDsCSV(WebAppTest):
    """
    1. Test flow:
    2. Login to the LMS
    3. Choose a course
    4. Go to the Instructor dashboard
    5. "Data Download" tab
    6. Click "get student anonymized IDs CSV" button
    """
    DEMO_COURSE_USER = os.environ.get('USER_LOGIN_EMAIL')
    DEMO_COURSE_PASSWORD = os.environ.get('USER_LOGIN_PASSWORD')

    def setUp(self):
        """
        Initialize the page object
        """
        super(StaffDownloadAnonymizedIDsCSV, self).setUp()

        self.login_page = LmsLogin(self.browser)
        self.dashboard = DashboardPageExtended(self.browser)

        self.course_data = get_course_info()
        self.course_info = get_course_key(self.course_data)
        self.course_page = CourseInfoPageExtended(self.browser, self.course_info)

    def test_flow(self):
        """
        Staff ->DataDownload->DownloadCSVanonymizedStudentIDs

        """
        # Login
        self.login_page.visit()
        self.login_page.login(self.DEMO_COURSE_USER, self.DEMO_COURSE_PASSWORD)
        self.dashboard.visit()
        # switch to Instructor tab
        self.dashboard.select_course_by_id('course-v1:orgX+FE6778+2015_T2')
        nav_tab_page = CourseInfoPageExtended(self.browser, self.course_info)
        nav_tab_page.go_to_tab('Instructor')
        nav_tab_page.wait_for_page()
        nav_tab_page.browser.refresh()

        # switch to Data Download tab
        instructor_dashboard = InstructorDashboardPageExtended(self.browser, self.course_info)
        instructor_dashboard.select_data_download()
        # click on download Get Student Anonymized IDs CSV

        data_download_page = DataDownloadPageExtended(self.browser)
        data_download_page.generate_student_anonymized_idscsv.click()
        data_download_page.get_available_reports_for_download()
