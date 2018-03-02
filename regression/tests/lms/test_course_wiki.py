from bok_choy.web_app_test import WebAppTest
from regression.tests.helpers.api_clients import LmsLoginApi
from regression.pages.lms.course_wiki_page import WikiPage
from regression.pages.lms.utils import get_course_key
from regression.tests.helpers.utils import (
    get_course_info)


class WikiTest(WebAppTest):
    """
    Test to check that wiki page is available
    """

    def setUp(self):
        super(WikiTest, self).setUp()
        self.course_info = get_course_info()
        self.wiki_page = WikiPage(self.browser, get_course_key(self.course_info))

    def test_course_wiki_page(self):
        login_api = LmsLoginApi()
        login_api.authenticate(self.browser)

        self.wiki_page.visit()
        self.wiki_page.wait_for_page()
        while self.wiki_page.is_browser_on_page():
            break
