import os

from unittest import skip
from bok_choy.web_app_test import WebAppTest

from regression.pages.lms.dashboard_lms import DashboardPageExtended
from regression.pages.lms.register_page import RegisterPageExtended
import regression.tests.helpers.utils as Helper
from regression.tests.helpers.api_clients import GuerrillaMailApi
from edxapp_acceptance.pages.lms.login_and_register import ResetPasswordPage
from regression.pages.lms.reset_password_confirm_page import ResetPasswordConfirmPage
from regression.pages.lms.reset_password_complete_page import PasswordCompletePage
from regression.pages.lms import LMS_PROTOCOL


class TestNewUserRegistration(WebAppTest):
    """
    Register a new user and activate account
    """

    DEMO_COURSE_USER = os.environ.get('USER_LOGIN_EMAIL')
    DEMO_COURSE_PASSWORD = os.environ.get('USER_LOGIN_PASSWORD')
    LMS_BASE_URL = os.environ.get('LMS_BASE_URL')
    EMO_COURSE_PASSWORD = os.environ.get('USER_LOGIN_PASSWORD')

    creds = Helper.get_random_credentials()
    GuerillaMail = GuerrillaMailApi(creds[0])
    generate_email = GuerillaMail.user_email

    def setUp(self):
        """
        Initialize the page object
        """
        super(TestNewUserRegistration, self).setUp()
        self.user_registration = RegisterPageExtended(self.browser)
        self.dashboard_page = DashboardPageExtended(self.browser)
        self.forgot_password_page = ResetPasswordPage(self.browser)

    @skip(
        'need to fix guerrillamail'
    )
    def test_1_register_user(self):
        """
        Test that new user can be registered using Guerilla Mail API
        and newly created account can be activated

        """
        self.user_registration.visit()

        self.user_registration.is_browser_on_page()
        self.user_registration.register_user(
            email=self.generate_email,
            password='123456',
            country='US',
            username=self.creds[0],
            full_name='name',
            terms_of_service=True,
        )
        self.dashboard_page.is_browser_on_page()

        Helper.activate_account_updated(self, self.GuerillaMail)

    @skip(
        'need to fix guerrillamail'
    )
    def test_2_forgot_password(self):
        """
        Test that just registered user can reset own password

        """
        self.forgot_password_page.url = LMS_PROTOCOL + '://' + self.LMS_BASE_URL + "/login#forgot-password-modal"
        self.forgot_password_page.visit()
        self.forgot_password_page.is_browser_on_page()
        self.forgot_password_page.is_form_visible()
        self.forgot_password_page.fill_password_reset_form(self.generate_email)
        self.forgot_password_page.is_success_visible('.submission-success')
        self.assertEqual(self.forgot_password_page.get_success_message(), [u'Check Your Email'])

        url = self.GuerillaMail.get_url_from_email('password_reset_confirm')

        self.reset_password_page = ResetPasswordConfirmPage(self.browser, url)
        self.reset_password_page.visit()
        self.reset_password_page.is_browser_on_page()
        self.reset_password_page.reset_password('qwerty')
        PasswordCompletePage(self.browser).is_browser_on_page()
