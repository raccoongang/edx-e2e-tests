import os
from unittest import skip

from bok_choy.web_app_test import WebAppTest
from regression.pages.lms.index import IndexPageExtended


class CourseSearchAnonymous(WebAppTest):
    '''
    As an Anonymous user I want to be able to search for Courses of Explore course page
    '''
    def setUp(self):
        super(CourseSearchAnonymous, self).setUp()
        self.index_page = IndexPageExtended(self.browser)
        self.COURSE_DISPLAY_NAME = os.environ.get('SEARCH_COURSE_DISPLAY_NAME', 'RACCOON GANG DEMO')

    def test_course_search_anonymous(self):
        self.index_page.visit()
        self.index_page.wait_for_page()
        self.index_page.search(self.COURSE_DISPLAY_NAME)
        self.index_page.wait_for_element_visibility('.courses','Waiting for the course search')
        self.index_page.wait_for_element_presence('.active-filter','Waiting for the tag')
        self.assertIn(
            self.COURSE_DISPLAY_NAME.upper(),
            self.index_page.q(css='.active-filter')[0].text.upper()
        )
        search_results = self.index_page.q(css='.courses-listing').text

        for result in search_results:
            if self.COURSE_DISPLAY_NAME.upper() in result or\
                self.COURSE_DISPLAY_NAME in result:
                break
        else:
            raise Exception('Error! Search results not found')

        self.index_page.q(css='#clear-all-filters').click()
        self.index_page.wait_for_element_absence('[class="facet-option discovery-button"]','waiting for the tag to disappear')
