import os

from edxapp_acceptance.pages.lms.index import IndexPage
from regression.pages.lms import LOGIN_BASE_URL


BANNER_SELECTOR = 'section.home header div.outer-wrapper div.title .heading-group h1'

class IndexPageExtended(IndexPage):

    url = LOGIN_BASE_URL

    def is_browser_on_page(self):
        """
        Returns a browser query object representing the video modal element
        """
        element = self.q(css=BANNER_SELECTOR)
        return element.visible and element.text[0].startswith("TIPS FOR BETTER TIME MANAGEMENT")

    def search(self, course_name):
        self.q(css='[name="search_query"]').fill(course_name)
        self.q(css='.search-button').click()



