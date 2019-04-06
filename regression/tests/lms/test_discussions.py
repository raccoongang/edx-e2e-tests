import time
import unittest
from uuid import uuid4

from bok_choy.web_app_test import WebAppTest
from bok_choy.page_object import WrongPageError
from bok_choy.page_object import PageLoadError

from edxapp_acceptance.pages.lms.discussion import DiscussionThreadPage

from regression.pages.lms.discussions_page import DiscussionsHomePageExtended
from regression.pages.lms.discussions_page import DiscussionThreadPageExtended
from regression.tests.helpers.api_clients import LmsLoginApi
from regression.tests.helpers.utils import get_course_info
from regression.pages.lms.utils import get_course_key


class DiscussionTest(WebAppTest):
    """
    Test to check that discussion page is available
    """

    def setUp(self):
        super(DiscussionTest, self).setUp()

        login_api = LmsLoginApi()
        login_api.authenticate(self.browser)
        self.discussion_thread_page = DiscussionThreadPage(self.browser, '.page-content')

        self.discussion_home_page_ext = DiscussionsHomePageExtended(self.browser, get_course_key(get_course_info()))

        self.post_title = 'post_to_test{}'.format(uuid4().hex)
        self.description = 'description{}'.format(uuid4().hex)
        self.response = 'test response{}'.format(uuid4().hex)
        self.comment = 'comment{}'.format(uuid4().hex)

        try:
            self.discussion_home_page_ext.visit()
        except PageLoadError:
            raise unittest.SkipTest('The Discussions page isnt available')
        self.discussion_home_page_ext.is_browser_on_page()

    def test_discussion_page(self):
        """
        Tests discussions page:
        1. Post can be added/edited/deleted
        2. Response to the post can be added/deleted
        3. Comment to the response can be added/deleted
        4. Test following
        5. Test Search
        """
        #add new post
        self.discussion_home_page_ext.click_new_post_button()
        self.discussion_home_page_ext.fill_post_form(self.post_title, self.description)

        #search_for_created post
        self.discussion_home_page_ext.perform_search(self.post_title)
        self.discussion_home_page_ext.perform_search(self.post_title)
        self.discussion_home_page_ext.wait_for_element_visibility('.forum-nav-thread-link .forum-nav-thread-wrapper-1 span.forum-nav-thread-title', 'perform_search')
        link = self.discussion_home_page_ext.get_the_thread_link()

        #visit thread page
        self.discussion_thread_page_ext = DiscussionThreadPageExtended(
            self.browser, get_course_key(get_course_info()), link=link)
        self.discussion_thread_page_ext.visit()

        #assert that user on the correct page
        post_title = self.discussion_thread_page_ext.get_post_title()
        self.assertEqual(''.join(post_title.text), self.post_title)

        #check that post is followed
        last_follow_post = self.discussion_thread_page_ext.last_follow_post()
        self.assertEqual(last_follow_post, self.post_title)

        #check that post can be unfollowed
        followed_posts = self.discussion_thread_page_ext.unfollow_post()
        self.assertNotIn(self.post_title, followed_posts)

        #edit post
        text_post = 'post edited {}'.format(str(uuid4().hex))
        self.discussion_thread_page_ext.edit_post(text=text_post)
        self.discussion_home_page_ext.wait_for_element_visibility('div.post-header-content'.format(str(uuid4().hex)), 'post edited')
        post_title_edited = self.discussion_thread_page_ext.get_post_title()
        self.assertEqual(''.join(post_title_edited.text), text_post)

        #add a response
        self.discussion_thread_page_ext.add_response(self.response)

        #assert added reponse
        response_text = self.discussion_thread_page_ext.get_response_text()
        self.assertEqual(self.response, ''.join(response_text))

        #edit response
        text_response = 'response edited {}'.format(str(uuid4().hex))
        self.discussion_thread_page_ext.edit_response(text=text_response)
        self.discussion_home_page_ext.wait_for_element_visibility('div.post-extended-content.thread-responses-wrapper ol li div div p', 'response edited')
        response_text_edit = self.discussion_thread_page_ext.get_response_text()
        self.assertEqual(''.join(response_text_edit), text_response)

        #add comment
        self.discussion_thread_page_ext.add_comment(self.comment)
        self.discussion_home_page_ext.wait_for_element_visibility('#comment_unsaved', 'add comment')

        #assert_comment_is_visible
        self.assertTrue(self.discussion_thread_page_ext.is_comment_visible())

        #edit comment
        text_comment = 'comment edited {}'.format(str(uuid4().hex))
        self.discussion_thread_page_ext.edit_comment(text=text_comment)
        self.discussion_home_page_ext.wait_for_element_visibility('div.discussion-comment', 'comment edited')
        comment_text_edit = self.discussion_thread_page_ext.get_comment_text()
        self.assertEqual(''.join(comment_text_edit), text_comment)

        #delete comment
        self.discussion_thread_page_ext.delete_comment()

        #is_comment deleted
        self.discussion_thread_page_ext.is_comment_deleted()

        #delete response
        self.discussion_thread_page_ext.delete_response()
        self.discussion_thread_page_ext.is_response_deleted()

        #delete post
        try:
            self.discussion_thread_page_ext.delete_post()
            self.discussion_thread_page_ext.wait_for_element_absence('div.discussion-article', 'post delete')
        except WrongPageError:
            pass
        finally:
            if self.discussion_thread_page_ext.q(css='.response-body p').visible:
                raise Exception('Response isnt deleted')
