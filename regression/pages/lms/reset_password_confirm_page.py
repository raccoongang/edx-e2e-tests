"""
Forgot Password confirm page
"""
from bok_choy.page_object import PageObject


class ResetPasswordConfirmPage(PageObject):
    """
    This class describes forgot password confirm page

    """

    def __init__(self, browser, link):
        super(ResetPasswordConfirmPage, self).__init__(browser)
        self.link = link

    def is_browser_on_page(self):
        return self.q(css='form[id="passwordreset-form"]').present

    @property
    def url(self):
        return self.link

    def reset_password(self, password):
        new_password = self.q(css='#new_password1')
        new_password.fill(password)

        confirm_passoword = self.q(css='#new_password2')
        confirm_passoword.fill(password)

        self.q(css=".action.action-primary.action-update.js-reset").click()
