"""
Course info page
"""
import re
from edxapp_acceptance.pages.lms.course_page import CoursePage
from regression.pages.lms import LOGIN_BASE_URL
from regression.pages.lms.utils import get_course_key
from regression.tests.helpers.utils import (
    get_course_info)


class CourseInfoPageExtended(CoursePage):
    """
    This class is an extended class of CourseInfoPage,
    where we add methods that are different or not used in CourseInfoPage
    """
    URL_MATCH_PATTERN = r'(http(s*)\:\/\/(.[^\/]+)/courses/(.[^\/]+)/(\w+))'
    url_path = "info"

    @property
    def url(self):
        """
        Construct a URL to the page within the course.
        """
        course_info = get_course_info()
        course_key = get_course_key(course_info)
        return "{}/courses/{}/{}".format(
            LOGIN_BASE_URL, course_key, self.url_path)

    def click_resume_button(self):
        """
        Clicks Resume button of the course selected
        """
        self.q(css='.last-accessed-link').first.click()

    def go_to_tab(self, tab_name):
        """
        Navigate to the tab `tab_name`.
        """
        for el in self.browser.find_elements_by_class_name('tab'):
            if el.find_element_by_tag_name("a").text.split("\n")[0] == tab_name:
                el.find_element_by_tag_name("a").click()
                return

    def is_browser_on_page(self):
        assert re.match(self.URL_MATCH_PATTERN, self.browser.current_url) is not None
        return True

    def switch_preview_mode_to(self, mode_name):
        options = \
            self.browser.find_element_by_class_name("action-preview-select").find_elements_by_tag_name("option")
        for opt in options:
            if opt.text.lower() == mode_name:
                opt.click()
                break
