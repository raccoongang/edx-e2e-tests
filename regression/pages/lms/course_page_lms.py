"""
Course Home page
"""
import re
from edxapp_acceptance.pages.lms.course_home import CourseHomePage
from regression.pages.lms import LOGIN_BASE_URL
from regression.pages.lms.utils import get_course_key
from regression.tests.helpers.utils import (
    get_course_info)


class CourseHomePageExtended(CourseHomePage):
    """
    This class is an extended class of CourseHomePage,
    where we add methods that are different or not used in CourseHomePage
    """
    @property
    def url(self):
        """
        Construct a URL to the page within the course.
        """
        return "{}/courses/{}/{}".format(
            LOGIN_BASE_URL, self.course_id, self.url_path
        )

    def is_browser_on_page(self):
        return self.q(css='.course-tabs').present

    def click_resume_button(self):
        """
        Clicks Resume button of the course selected
        """
        self.q(css='.action-resume-course span').first.click()

    def go_to_tab(self, tab_name):
        """
        Navigate to the tab `tab_name`.
        """
        for el in self.browser.find_elements_by_class_name('tab'):
            if el.find_element_by_tag_name("a").text.split("\n")[0] == tab_name:
                el.find_element_by_tag_name("a").click()
                return

    def switch_preview_mode_to(self, mode_name):
        self.browser.find_element_by_id("action-preview-select").\
            find_element_by_css_selector('option[value="{}"]'.format(mode_name)).click()

class CourseInfoPageExtended(CourseHomePage):
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

    def is_browser_on_page(self):
        assert re.match(self.URL_MATCH_PATTERN, self.browser.current_url) is not None
        return True