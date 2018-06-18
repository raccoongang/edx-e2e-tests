"""
Course info page
"""
from edxapp_acceptance.pages.lms.course_info import CourseInfoPage
from regression.pages.lms import LOGIN_BASE_URL
from regression.pages.lms.utils import get_course_key
from regression.tests.helpers.utils import (
    get_course_info)


class CourseInfoPageExtended(CourseInfoPage):
    """
    This class is an extended class of CourseInfoPage,
    where we add methods that are different or not used in CourseInfoPage
    """

    @property
    def url(self):
        """
        Construct a URL to the page within the course.
        """
        course_info = get_course_info()
        course_key = get_course_key(course_info)
        return "{}/courses/{}/{}".format(
            LOGIN_BASE_URL, course_key, self.url_path
        )

    def click_resume_button(self):
        """
        Clicks Resume button of the course selected
        """
        self.q(css='.last-accessed-link').first.click()
