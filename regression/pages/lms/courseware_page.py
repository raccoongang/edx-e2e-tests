from edxapp_acceptance.pages.lms.courseware import CoursewarePage

from regression.pages.lms import LOGIN_BASE_URL

class CoursewarePageExtended(CoursewarePage):

    def __init__(self, browser, course_id):
        super(CoursewarePageExtended, self).__init__(browser, course_id)
        self.course_id = course_id

    @property
    def url(self):
        """
        Construct a URL to the page
        """
        return '{}/courses/{}/{}'.format(LOGIN_BASE_URL, self.course_id, self.url_path)
