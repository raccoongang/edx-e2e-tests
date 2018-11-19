from edxapp_acceptance.pages.lms.course_info import CourseInfoPage
from regression.pages.lms import LOGIN_BASE_URL


class CourseInfoPageExtended(CourseInfoPage):
    """
    Extends from CourseInfoPage page object
    """

    def __init__(self, browser, course_id):
        super(CourseInfoPageExtended, self).__init__(browser, course_id)

    @property
    def url(self):
        """
        Construct a URL to the page within the course.
        """
        return LOGIN_BASE_URL + "/courses/" + self.course_id + "/" + self.url_path

    def get_text_of_updates(self):
        return self.q(css='.toggle-visibility-element.article-content ')

    def get_text_of_handouts(self):
        handouts = self.q(css='.handouts').text
        str_handouts = ''.join(handouts)
        handout_text = str_handouts.split('\n')[-1:]
        return ''.join(handout_text)
