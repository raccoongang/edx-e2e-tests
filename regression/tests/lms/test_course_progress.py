from bok_choy.web_app_test import WebAppTest
from regression.pages.lms.progress_page import ProgressPageExtended
from regression.tests.helpers.utils import (
    get_course_info)

from regression.tests.helpers.api_clients import LmsLoginApi
from regression.pages.lms.utils import get_course_key
from regression.pages.studio.studio_home import DashboardPageExtended
from regression.pages.lms.instructor_dashboard import InstructorDashboardPageExtended


class CourseProgressTest(WebAppTest):
    """
    E2E test that we can visit pages in the Selected Course.
    """
    def setUp(self):
        super(CourseProgressTest, self).setUp()
        self.course_info = get_course_key(get_course_info())
        self.progress_page = ProgressPageExtended(self.browser, self.course_info)
        self.instructor_page = InstructorDashboardPageExtended(self.browser, self.course_info)
        login_api = LmsLoginApi()
        login_api.authenticate(self.browser)


    def test_course_progress_pages(self):
        """
        Verifies that user can navigate to LMS Pages
        """
        self.progress_page.visit()
        self.assertIn(
            "Course Progress for Student",
            self.progress_page.q(css='h3.hd.hd-3.progress-certificates-title')[0].text
        )

        self.assertEquals(
            self.progress_page.q(css='#chapter_1')[0].text,
            "Example Week 1: Getting Started"
        )

        self.assertIn(
            "Lesson 1 - Getting Started",
            self.progress_page.q(css='section[aria-labelledby="chapter_1"] h5.hd.hd-5 a')[0].text
        )

        self.assertEquals(
            self.progress_page.q(css='section[aria-labelledby="chapter_1"] dt.hd.hd-6')[0].text,
            "Practice Scores:"
        )

        # self.assertEquals(
        #     self.progress_page.q(css='section[aria-labelledby="chapter_0"] div:nth-child(even) dt.hd.hd-6')[0].text,
        #     "Problem Scores:"
        # )

    def test_progress_page_for_a_learner_by_instructor(self):

        self.instructor_page.visit()
        self.instructor_page.q(css='[data-section="student_admin"]').first.click()

        username = "staff"
        self.instructor_page.q(css='[name="student-select-progress"]').fill(username)
        self.instructor_page.q(css='a.progress-link[href=""]').first.click()
        self.instructor_page.wait_for_ajax()

        self.assertIn(
            "Course Progress for Student 'staff' (staff@example.com)",
            self.instructor_page.q(css='h3.hd.hd-3.progress-certificates-title')[0].text
        )

        self.assertTrue(self.instructor_page.q(css='canvas.overlay').visible)
