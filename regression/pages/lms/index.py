import os

from edxapp_acceptance.pages.lms.index import IndexPage
from regression.pages.lms import LOGIN_BASE_URL


BANNER_SELECTOR = '.slick-list'

class IndexPageExtended(IndexPage):

    url = LOGIN_BASE_URL

    def is_browser_on_page(self):
        """
        Returns a browser query object representing the video modal element
        """
        return self.q(css=BANNER_SELECTOR).visible

    def search(self, course_name):
        self.q(css='[name="search_query"]').fill(course_name)
        self.q(css='.search-button[tabindex="0"]').click()
