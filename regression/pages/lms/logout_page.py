from bok_choy.page_object import PageObject

from regression.pages.lms import LOGIN_BASE_URL


class LogOutPage(PageObject):

    url = LOGIN_BASE_URL + '/logout'

    def is_browser_on_page(self):
        """
        Verifies if the browser is on the correct page
        """
        return self.q(css='.tab-nav-link[href="/login"]')
