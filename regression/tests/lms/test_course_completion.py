import unittest
import time

from bok_choy.web_app_test import WebAppTest
from bok_choy.page_object import PageLoadError

import regression.tests.helpers.utils as Helper
from regression.tests.helpers.api_clients import GuerrillaMailApi

from regression.pages.lms.dashboard_lms import DashboardPageExtended
from regression.pages.lms.register_page import RegisterPageExtended
import regression.tests.helpers.utils as Helper
from regression.tests.helpers.api_clients import GuerrillaMailApi
from edxapp_acceptance.pages.lms.login_and_register import ResetPasswordPage
from regression.pages.lms.logout_page import LogOutPage

from regression.pages.whitelabel.dashboard_page import DashboardPageExtended

from regression.pages.lms.reset_password_confirm_page import ResetPasswordConfirmPage
from regression.pages.lms.reset_password_complete_page import PasswordCompletePage
from regression.pages.lms import LMS_PROTOCOL


class Test(WebAppTest):

    amount_of_users = 10

    def setUp(self):
        super(Test, self).setUp()
        self.user_registration = RegisterPageExtended(self.browser)
        self.dashboard_page = DashboardPageExtended(self.browser)
        self.forgot_password_page = ResetPasswordPage(self.browser)
        self.logout_page = LogOutPage(self.browser)


    def register_user(self):
        """
        Test that new user can be registered using Guerilla Mail API
        and newly created account can be activated

        """
        creds = Helper.get_random_credentials()
        GuerillaMail = GuerrillaMailApi(creds[0])
        generate_email = GuerillaMail.user_email


        self.user_registration.visit()

        try:
            self.user_registration.is_browser_on_page()
        except PageLoadError:
            self.user_registration.visit()

        self.user_registration.register_user(
            email=generate_email,
            password='123456',
            country='USA',
            username=creds[0],
            full_name='name',
            terms_of_service=True,
        )
        self.dashboard_page.is_browser_on_page()

        Helper.activate_account_updated(self, GuerillaMail)

        return generate_email

    def test_register_user_count(self):
        i = 1
        users = {}
        while i < self.amount_of_users:
            register_user = self.register_user()

            self.logout_page.visit()

            user_email = register_user
            users[i] = user_email
            i = i + 1
            print(users)


            #try to use button. cause visit method returns exception