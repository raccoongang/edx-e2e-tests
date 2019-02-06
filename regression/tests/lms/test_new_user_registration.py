import os

from bok_choy.web_app_test import WebAppTest
from regression.pages.lms.login_lms import LmsLogin
from regression.pages.lms.account_settings_page import AccountSettingsPageExtended
from regression.pages.lms.dashboard_lms import DashboardPageExtended
from regression.pages.lms.register_page import RegisterPageExtended
import regression.tests.helpers.utils as Helper
from regression.tests.helpers.api_clients import GuerrillaMailApi


class TestNewUserRegistration(WebAppTest):
    """
    Register a new user and activate account
    """

    DEMO_COURSE_USER = os.environ.get('USER_LOGIN_EMAIL')
    DEMO_COURSE_PASSWORD = os.environ.get('USER_LOGIN_PASSWORD')
    LMS_BASE_URL = os.environ.get('LMS_BASE_URL')
    password = '123456'
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
        self.login_page = LmsLogin(self.browser)
        self.setting_page = AccountSettingsPageExtended(self.browser)

    def test_register_user(self):
        """
        Test that new user can be registered using Guerilla Mail API
        and newly created account can be activated

        """
        self.user_registration.visit()

        self.user_registration.is_browser_on_page()

        self.user_registration.register_user(
            email=self.generate_email,
            password=self.password,
            country='US',
            username=self.creds[0],
            full_name='name',
            terms_of_service=True,
        )
        self.dashboard_page.is_browser_on_page()

        Helper.activate_account_updated(self, self.GuerillaMail)

    def test_reset_email(self):
        """
        Test reset email
        """
        self.login_page.visit()
        self.login_page.login(self.generate_email, self.password)
        self.assertEqual(
            self.login_page.q(
                css='.wrapper-header-courses .header-courses').text[0].lower(),
            'my courses',
            msg='User not logged in as expected.')

        self.setting_page.visit()
        creds = Helper.get_random_credentials()
        GuerillaMail = GuerrillaMailApi(creds[0])
        new_generate_email = GuerillaMail.user_email
        self.setting_page.reset_email_field(new_generate_email)

        Helper.reset_email_activate_updated(self, GuerillaMail)
