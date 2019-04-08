import os

from bok_choy.web_app_test import WebAppTest

from regression.pages.lms.utils import get_course_key
from regression.pages.lms.course_about_page import CourseAboutPageExtended
from regression.tests.helpers.api_clients import LmsLoginApi
from regression.tests.helpers.utils import get_course_info
from edxapp_acceptance.pages.lms.dashboard_search import DashboardSearchPage


class DashboardSearchTest(WebAppTest):
    """
    Test to check search on the dashboard page
    """
    def setUp(self):
        super(DashboardSearchTest, self).setUp()
        self.course_info = get_course_key(get_course_info())
        self.course_about_page = CourseAboutPageExtended(self.browser, self.course_info)

        self.course_about_page.visit()
        self.course_about_page.enroll_if_unenroll()

    def test_dashboard_search(self):
        login_api = LmsLoginApi()
        login_api.authenticate(self.browser)

        dashboard_search_page = DashboardSearchPage(self.browser)
        try:
            dashboard_search_page.is_browser_on_page()
        except False:
            print('ERROR: search is not available on the page')
        COURSE_SECTION_NAME = 'Introduction'
        dashboard_search_page.search_for_term(text=COURSE_SECTION_NAME)

        search_results = dashboard_search_page.search_results.text

        for i in search_results:
            if 'edX Demonstration Course' in i:
                break
        else:
            raise Exception('Error! Search results not found')
