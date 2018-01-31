import os

from bok_choy.web_app_test import WebAppTest

from regression.tests.helpers.api_clients import LmsLoginApi
from edxapp_acceptance.pages.lms.dashboard_search import DashboardSearchPage


class DashboardSearchTest(WebAppTest):
    """
    Test to check search on the dashboard page
    """

    def test_dashboard_search(self):
        login_api = LmsLoginApi()
        login_api.authenticate(self.browser)

        dashboard_search_page = DashboardSearchPage(self.browser)
        try:
            dashboard_search_page.is_browser_on_page()
        except False:
            print('ERROR: search is not available on the page')

        COURSE_DISPLAY_NAME = os.environ.get('COURSE_DISPLAY_NAME', 'demo course')
        dashboard_search_page.search_for_term(text=COURSE_DISPLAY_NAME)

        search_results = dashboard_search_page.search_results.text

        for i in search_results:
            if 'edX Demonstration Course' in i:
                break
        else:
            raise Exception('Error! Search results not found')
