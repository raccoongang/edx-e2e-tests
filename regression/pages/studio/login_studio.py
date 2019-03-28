"""
Studio login page
"""
from edxapp_acceptance.pages.studio.login import LoginPage
from regression.pages.studio import LOGIN_BASE_URL
from bok_choy.promise import EmptyPromise


class StudioLogin(LoginPage):
    """
    This class is an extended class of LoginPage.
    """
    url = LOGIN_BASE_URL + '/signin'

    def is_browser_on_page(self):
        return self.q(css="[id=login_form]").present

    def login(self, email, password, expect_success=True):
        """
        Attempt to log in using 'email' and 'password'.
        """
        self.wait_for_element_visibility('#field-email', 'Email field is shown')
        self.q(css="#email").fill(email)

        self.q(css="#password").fill(password)
        self.q(css="#submit").click()

        # Ensure that we make it to another page
        if expect_success:
            EmptyPromise(
                lambda: "login" not in self.browser.current_url,
                "redirected from the login page"
            ).fulfill()
