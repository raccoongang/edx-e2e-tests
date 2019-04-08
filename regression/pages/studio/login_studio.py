"""
Studio login page
"""
from time import sleep

from edxapp_acceptance.pages.studio.login import LoginPage
from regression.pages.studio import LOGIN_BASE_URL


class StudioLogin(LoginPage):
    """
    This class is an extended class of LoginPage.
    """
    url = LOGIN_BASE_URL + '/signin'

    def is_browser_on_page(self):
        return self.q(css="[id=login_form]").present

    def login(self, email, password):
        """
        Attempt to log in using 'email' and 'password'.
        """
        self.wait_for_element_visibility('#field-email', 'Email field is shown')
        self.q(css="#email").fill(email)
        self.fill_password(password)
        sleep(1)
        self.q(css="#submit").click()

    def fill_password(self, password):
        """
        Fill the password field with the value.
        """
        self.q(css="#password").fill(password)
