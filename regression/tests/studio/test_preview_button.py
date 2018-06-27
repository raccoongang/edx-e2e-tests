"""
End to end tests for preview button
"""
import os
from unittest import skipIf

from bok_choy.web_app_test import WebAppTest

from edxapp_acceptance.pages.studio.container import ContainerPage

from regression.pages.studio.studio_home import DashboardPageExtended
from regression.pages.studio.login_studio import StudioLogin
from regression.pages.studio.course_outline_page import CourseOutlinePageExtended
from regression.pages.studio.preview_page import PreviewPage


class TestPreviewButton(WebAppTest):
    """
    Test for preview button in a course
    """

    DEMO_COURSE_USER = os.environ.get('USER_LOGIN_EMAIL')
    DEMO_COURSE_PASSWORD = os.environ.get('USER_LOGIN_PASSWORD')
    COURSE_NUMBER = os.environ.get('COURSE_NUMBER', 'DemoX')

    def setUp(self):
        """
        Initialize the page object
        """
        super(TestPreviewButton, self).setUp()
        self.studio_login_page = StudioLogin(self.browser)
        self.studio_home_page = DashboardPageExtended(self.browser)
        self.course_page = CourseOutlinePageExtended(
            self.browser, 'org', 'number', 'run')
        self.container_page = ContainerPage(self.browser, locator='')
        self.preview_page = PreviewPage(self.browser)

    def test_preview_button(self):
        """
        Verifies that user can click the preview button and open the preview page
        """
        self.studio_login_page.visit()
        self.studio_login_page.login(self.DEMO_COURSE_USER, self.DEMO_COURSE_PASSWORD)
        self.studio_home_page.wait_for_page()
        self.studio_home_page.is_browser_on_page()

        self.studio_home_page.select_course_by_number(self.COURSE_NUMBER)

        self.course_page.wait_for_page()
        self.course_page.expand_subsections()
        self.course_page.wait_for_page()

        self.course_page.open_unit()
        self.container_page.is_browser_on_page()
        self.container_page.preview()

        self.preview_page.is_browser_on_page()
        assert 'preview' in self.browser.current_url