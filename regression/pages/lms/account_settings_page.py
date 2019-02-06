from edxapp_acceptance.pages.lms.account_settings import AccountSettingsPage
from regression.pages.lms import LOGIN_BASE_URL


class AccountSettingsPageExtended(AccountSettingsPage):
    """
    Tests
    """
    url = LOGIN_BASE_URL + '/account/settings'

    def reset_email_field(self, value):
        self.q(css='#field-input-email').fill(value)
        self.q(css='#u-field-message-email').click()
