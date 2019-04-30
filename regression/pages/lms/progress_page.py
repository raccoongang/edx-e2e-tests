from edxapp_acceptance.pages.lms.progress import ProgressPage
from regression.pages.lms import LOGIN_BASE_URL

class ProgressPageExtended(ProgressPage):

    @property
    def url(self):
        return "{}/courses/{}/{}".format(
            LOGIN_BASE_URL, self.course_id, self.url_path)

    @property
    def header(self):
        return self.q(css='.hd.hd-2.progress-certificates-title')[0].text
