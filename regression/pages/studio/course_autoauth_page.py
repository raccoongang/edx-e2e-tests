from edxapp_acceptance.pages.common.auto_auth import AutoAuthPage


from regression.pages.studio import LOGIN_BASE_URL


class AutoAuthPageExtended(AutoAuthPage):


    """
    This class is an extended class of LoginPage.
    """
    url = LOGIN_BASE_URL

    def is_browser_on_page(self):
        return self.q(css="[id=login_form]").present





