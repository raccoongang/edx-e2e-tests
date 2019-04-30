"""
Courseware Boomarks
"""
from common.test.acceptance.pages.common.paging import PaginatedUIMixin
from edxapp_acceptance.pages.lms.bookmarks import BookmarksPage
from regression.pages.lms import LOGIN_BASE_URL

class BookmarksPageExtended(BookmarksPage):
    """
    Courseware Bookmarks Page.
    """
    @property
    def url(self):
        """
        Construct a URL to the page within the course.
        """
        return "{}/courses/{}/{}".format(
            LOGIN_BASE_URL, self.course_id, self.url_path
        )
