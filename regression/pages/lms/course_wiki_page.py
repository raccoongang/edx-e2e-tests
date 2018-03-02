"""
Wiki page
"""

from edxapp_acceptance.pages.lms.course_wiki import CourseWikiPage
from regression.pages.lms import LOGIN_BASE_URL


class WikiPage(CourseWikiPage):
    """
    This class is an extended class of Course Wiki page,

    """

    @property
    def url(self):
        return "{}/courses/{}/{}".format(
            LOGIN_BASE_URL, self.course_id, self.url_path)
