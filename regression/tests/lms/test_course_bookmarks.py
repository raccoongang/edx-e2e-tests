"""
End to end tests course booksmarks.
"""
from bok_choy.web_app_test import WebAppTest

from regression.pages.lms.course_bookmarks_page import BookmarksPageExtended
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
        self.bookmarks_page = BookmarksPageExtended(self.browser, self.course_info)
        self.courseware_page = CoursewarePageExtended(self.browser, self.course_info)

        lms_login = LmsLoginApi()
        lms_login.authenticate(self.browser)

    def test_course_bookmarks(self):
        """
        Check bookmarks add
        """
        # Open bookmarks page and check count of bookmarks
        self.bookmarks_page.visit()
        amount_of_bookmarks = self.bookmarks_page.count()

        # Open courseware and proceed to the first unit
        self.courseware_page.visit()

        # Add bookmark
        # Go to /bookmarks and assert that counter of bookmarks changes
        if ''.join(self.courseware_page.add_bookmark()) == u'Bookmarked':
            self.bookmarks_page.visit()
            self.assertEqual(self.bookmarks_page.count() - amount_of_bookmarks, 1)

        else:
            self.assertEqual(''.join(self.courseware_page.add_bookmark()), u'Bookmarked')
            self.bookmarks_page.visit()
            self.assertEqual(self.bookmarks_page.count(), amount_of_bookmarks)
