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
        self.courseware_page = CoursewarePageExtended(self.browser, self.course_info)

        lms_login = LmsLoginApi()
        lms_login.authenticate(self.browser)

    def test_course_bookmarks(self):
        """
        Check bookmarks add
        """
        # Open bookmarks page and check count of bookmarks
        self.courseware_page.visit()
        self.courseware_page.wait_for_page()
        self.courseware_page.q(css='[class="courseware-bookmarks-button"]').click()
        old_count_bookmarks = len(self.courseware_page.q(css='.bookmarks-results-list .bookmarks-results-list-item').results)
        # Open courseware and proceed to the first unit
        self.courseware_page.visit()
        self.courseware_page.wait_for_page()
        # Add bookmark
        # Go to 'bookmarks' and assert that counter of bookmarks changes
        if ''.join(self.courseware_page.add_bookmark()) == u'Bookmarked':
            self.courseware_page.q(css='.bookmarks-list-button .is-inactive').click()
            new_count_bookmarks = len(self.courseware_page.q(css='.bookmarks-results-list .bookmarks-results-list-item').results)
            self.assertEqual(new_count_bookmarks - old_count_bookmarks, 1)

        else:
            self.assertEqual(''.join(self.courseware_page.add_bookmark()), u'Bookmarked')
            self.courseware_page.q(css='.bookmarks-list-button .is-inactive').click()
            new_count_bookmarks = len(self.courseware_page.q(css='.bookmarks-results-list .bookmarks-results-list-item').results)
            self.assertEqual(old_count_bookmarks - new_count_bookmarks, 1)
