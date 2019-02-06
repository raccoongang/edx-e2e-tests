from regression.pages.whitelabel.activate_account import ActivateAccount


class ActivateAccountExtended(ActivateAccount):

    def __init__(self, browser, activation_url):
        """
        Activate account url has to be set by the test
        """
        super(ActivateAccountExtended, self).__init__(browser, activation_url)
        self.activate_account_url = activation_url

    @property
    def url(self):
        """
        Construct URL of the page
        """
        return self.activate_account_url

    def is_browser_on_page(self):
        return self.q(css=self.activation_msg_css).present

    @property
    def is_account_activation_complete(self):
        """
        Is account activation complete?
        Returns:
            bool: True if activation complete message is visible:
        """
        return self.q(css=self.activation_msg_css).filter(
            lambda elem: 'activated' in elem.text
        ).visible

    def click_dashboard_from_drop_down_menu(self):
        """
        Clicks dashboard from the drop down menu
        """
        self.q(css='.user-name').click()
        self.q(css='.show-user-menu a[href="/dashboard"]').click()
