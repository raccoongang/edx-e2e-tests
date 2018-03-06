"""
Password Complete page
"""
from bok_choy.page_object import PageObject

from regression.pages.lms import LOGIN_BASE_URL


class PasswordCompletePage(PageObject):
    """
    This class is describes forgot password complete page

    """
    def url(self):
        return LOGIN_BASE_URL + '/password_reset_complete'

    def is_browser_on_page(self):
        return self.q(css='#password-reset-complete').present
