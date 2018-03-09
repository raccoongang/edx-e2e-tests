"""
Test for checking upload user avatar
"""
import os

from bok_choy.web_app_test import WebAppTest

from regression.tests.helpers.api_clients import LmsLoginApi
from regression.pages.lms.dashboard_lms import DashboardPageExtended
from regression.pages.lms.about_me_page import AboutMePage


class UserUploadPage(WebAppTest):
    """
    Verifies that user can update own avatar
    """

    DEMO_COURSE_USER = os.environ.get('USER_LOGIN_EMAIL')
    DEMO_COURSE_PASSWORD = os.environ.get('USER_LOGIN_PASSWORD')
    USERNAME = os.environ.get('username')

    def setUp(self):
        """
        Initialize the page object
        """
        super(UserUploadPage, self).setUp()
        self.login_api = LmsLoginApi()
        self.dashboard_ext = DashboardPageExtended(self.browser)
        self.about_me = AboutMePage(self.browser, self.USERNAME)

    def test_upload_avatar(self):
        self.login_api.authenticate(self.browser)
        self.dashboard_ext.is_browser_on_page()
        self.about_me.visit()
        self.about_me.is_browser_on_page()

        self.about_me.upload_image('upload_files/1.png')
