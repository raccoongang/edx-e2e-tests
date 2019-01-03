from bok_choy.web_app_test import WebAppTest
from regression.pages.lms.progress_page import ProgressPageExtended
from regression.tests.helpers.utils import (
    get_course_info)

from regression.tests.helpers.api_clients import LmsLoginApi
from regression.pages.lms.utils import get_course_key


class CourseProgressTest(WebAppTest):
    """
    E2E test that we can visit pages in the Selected Course.
    """
    def setUp(self):
        super(CourseProgressTest, self).setUp()
        self.course_info = get_course_key(get_course_info())
        self.progress_page = ProgressPageExtended(self.browser, self.course_info)

    def test_course_progress_pages(self):
        """
        Verifies that user can navigate to LMS Pages
        """
        # Log in as a student
        login_api = LmsLoginApi()
        login_api.authenticate(self.browser)

        self.progress_page.visit()
        self.assertIn(
            "Course Progress for Student",
            self.progress_page.q(css='h2.hd.hd-2.progress-certificates-title')[0].text
        )

        self.assertEquals(
            self.progress_page.q(css='#chapter_0')[0].text,
            "Example Week 1: Getting Started"
        )

        self.assertIn(
            "Lesson 1 - Getting Started",
            self.progress_page.q(css='section[aria-labelledby="chapter_0"] h4.hd.hd-4 a')[0].text
        )

        self.assertEquals(
            self.progress_page.q(css='section[aria-labelledby="chapter_0"] dt.hd.hd-6')[0].text,
            "Practice Scores:"
        )

        # self.assertEquals(
        #     self.progress_page.q(css='section[aria-labelledby="chapter_0"] div:nth-child(even) dt.hd.hd-6')[0].text,
        #     "Problem Scores:"
        # )
