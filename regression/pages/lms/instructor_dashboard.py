"""
Instructor dashboard page.
"""
from edxapp_acceptance.pages.lms.instructor_dashboard import (
    InstructorDashboardPage,
    DataDownloadPage
)
from regression.pages.lms import LOGIN_BASE_URL


class InstructorDashboardPageExtended(InstructorDashboardPage):
    """
    This class is an extended class of Instructor Dashboard Page
    """

    @property
    def url(self):
        """
        Construct a URL to the page within the course.
        """
        return "{}/courses/{}/{}".format(
            LOGIN_BASE_URL, self.course_id, self.url_path
        )

    def click_analytics_tab(self):
        """
        Clicks Analytics tab on Instructor Dashboard
        """
        self.q(css='[data-section="instructor_analytics"]').click()
        # Click initiates an ajax call
        self.wait_for_ajax()

    def get_insights_title_text(self):
        """
        Clicks edX Insights link on Analytics tab
        """
        self.q(css='p em a').click()
        self.browser.switch_to_window(self.browser.window_handles[-1])
        return self.q(css='.navbar-brand-app').text[0]


class DataDownloadPageExtended(DataDownloadPage):
    @property
    def generate_student_anonymized_idscsv(self):
        """
        Returns the "Generate Problem Grade Report" button.
        """
        if self.q(css='input[name=list-anon-ids]'):
            return self.q(css='input[name=list-anon-ids]')
        else:
            raise Exception('Error! Download (Get Student Anonymized IDs CSV button)  found')
