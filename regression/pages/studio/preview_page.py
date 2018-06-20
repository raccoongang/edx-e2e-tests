"""
Preview page.
"""
from bok_choy.page_object import PageObject


class PreviewPage(PageObject):
    """
    Preview page
    """
    url = ''

    def is_browser_on_page(self):
        return self.q(css='#login-form')
