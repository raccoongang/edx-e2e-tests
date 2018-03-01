import os

from bok_choy.web_app_test import WebAppTest

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

    def setUp(self):
        """
        Initialize the page object
        """
        super(TestNewUserRegistration, self).setUp()
        self.user_registration = RegisterPageExtended(self.browser)
        self.dashboard_page = DashboardPageExtended(self.browser)

    def test_register_user(self):
        """
        Test that new user can be registered using Guerilla Mail API
        and newly created account can be activated

        """
        self.user_registration.visit()
        creds = Helper.get_random_credentials()

        self.user_registration.is_browser_on_page()

        GuerillaMail = GuerrillaMailApi(creds[0])
        generate_email = GuerillaMail.user_email
        self.user_registration.register_user(
            email=generate_email,
            password='123456',
            country='USA',
            username=creds[0],
            full_name='name',
            terms_of_service=True,
        )
        self.dashboard_page.is_browser_on_page()

        Helper.activate_account_updated(self, GuerrillaMailApi(creds[0]))
