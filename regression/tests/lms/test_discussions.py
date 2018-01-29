import os

from bok_choy.web_app_test import WebAppTest

from regression.pages.lms import LMS_STAGE_BASE_URL, LMS_PROTOCOL
from regression.tests.helpers.api_clients import LmsLoginApi
from edxapp_acceptance.pages.lms.discussion import DiscussionThreadPage


class DiscussionTest(WebAppTest):
    """
    Test to check that discussion page is available
    """
    def test_course_discussion_page(self):
        LMS_BASE_URL = os.environ.get('LMS_BASE_URL', LMS_STAGE_BASE_URL)
        COURSE_ORG = os.environ.get('COURSE_ORG', 'edX')
        COURSE_NUMBER = os.environ.get('COURSE_NUMBER', 'DemoX')
        COURSE_RUN = os.environ.get('COURSE_RUN', 'Demo_Course')

        login_api = LmsLoginApi()
        login_api.authenticate(self.browser)
        discussion_page = DiscussionThreadPage(self.browser, '.page-content')

        discussion_page.url = '{}://{}/courses/course-v1:{}+{}+{}/discussion/forum/'.format(LMS_PROTOCOL, LMS_BASE_URL,
                            COURSE_ORG, COURSE_NUMBER, COURSE_RUN)

        discussion_page.visit()
        discussion_page.wait_for_page()
        discussion_page.is_browser_on_page()
