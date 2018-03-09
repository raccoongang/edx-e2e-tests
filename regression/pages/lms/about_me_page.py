"""
About me page
"""
from bok_choy.page_object import PageObject

from regression.pages.lms import LOGIN_BASE_URL


class AboutMePage(PageObject):
    """
    This class describes About me page

    """
    def __init__(self, browser, username):
        super(AboutMePage, self).__init__(browser)
        self.username = username

    def is_browser_on_page(self):
        return self.q(css='.wrapper-profile-sections.account-settings-container').present

    @property
    def url(self):
        return LOGIN_BASE_URL + '/u/{}#about_me'.format(self.username)

    def upload_image(self, path):
        file_input = self.q(css='.upload-button-input')
        file_input.fill(path)
