"""
End to end tests course booksmarks.
"""
import time
from bok_choy.web_app_test import WebAppTest

from regression.pages.lms.course_page_lms import CourseHomePageExtended
from regression.pages.lms.bookmarks import BookmarksPageExtended
from regression.pages.lms.lms_courseware import CoursewarePageExtended
from regression.tests.helpers.utils import (
    get_course_info)

from regression.tests.helpers.api_clients import LmsLoginApi
from regression.pages.lms.utils import get_course_key


class TestCourseBookmarks(WebAppTest):
    """
    Test to check that course bookmarks
    """

    def setUp(self):
        super(TestCourseBookmarks, self).setUp()
        self.course_info = get_course_key(get_course_info())
        self.course_page = CoursewarePageExtended(self.browser, self.course_info)
        self.bookmarks_page = BookmarksPageExtended(self.browser, self.course_info)
        lms_login = LmsLoginApi()
        lms_login.authenticate(self.browser)

    def test_course_bookmarks(self):
        """
        Check bookmarks add
        """
        # Open bookmarks page and check count of bookmarks
        self.bookmarks_page.visit()
        old_count_bookmarks = self.bookmarks_page.count()
        # Open courseware and proceed to the first unit
        self.course_page.visit()

        # Add bookmark
        # Go to /bookmarks and assert that counter of bookmarks changes
        if ''.join(self.course_page.add_bookmark()) == u'Bookmarked':
            self.bookmarks_page.visit()
            new_count_bookmarks = self.bookmarks_page.count()
            self.assertEqual(new_count_bookmarks - old_count_bookmarks, 1)

        else:
            self.bookmarks_page.visit()
            new_count_bookmarks = self.bookmarks_page.count()
            self.assertEqual(old_count_bookmarks - new_count_bookmarks, 1)
