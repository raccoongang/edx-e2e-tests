import time

from edxapp_acceptance.pages.lms.discussion import DiscussionTabHomePage
from regression.pages.lms import LOGIN_BASE_URL


class DiscussionsHomePageExtended(DiscussionTabHomePage):
    """
    Extends from Discussion Home Page
    """

    def __init__(self, browser, course_id):
        super(DiscussionsHomePageExtended, self).__init__(browser, course_id)
        self.course_id = course_id

    @property
    def url(self):
        """
        Construct a URL to the page
        """
        return '{}/courses/{}/{}'.format(LOGIN_BASE_URL, self.course_id, self.url_path)

    def fill_post_form(self, title_text, question_text):
        """
        Fill the create post form
        """
        title = self.q(css='.js-post-title.field-input')
        title.fill(title_text)
        question = self.q(css='.wmd-input')
        question.fill(question_text)

        self.scroll_to_element('.btn-brand.submit')
        self.q(css='.btn-brand.submit').click()

    def click_the_last_post(self):
        link = self.q(css='.forum-nav-thread a').attrs('href')[0]
        self.q(css='.forum-nav-thread a[href="{}"]'.format(link)).click()

    def wait_for_last_post_to_be_opened(self):
        self.wait_for_element_visibility('h2.post-title', 'Wait for title')

    def show_all_discussions(self):
        """ Show the list of all discussions. """
        self.q(css=".all-topics").click()

    def get_the_thread_id(self):
        try:
            thread_id_list = self.q(css='.forum-nav-thread-list li').attrs('data_id')
            return thread_id_list[0]
        except IndexError:
            return self.q(css='.forum-nav-thread-list li').attrs('data_id')[0]

    def get_the_thread_link(self):
        thread_id_list = self.q(css='.forum-nav-thread a').attrs('href')
        return thread_id_list[0]

    def _thread_is_rendered_successfully(self, thread_id):
        return self.q(css=".discussion-article[data-id='{}']".format(thread_id)).visible

    def click_and_open_thread(self, thread_id):
        """
        Click specific thread on the list.
        """
        self.q(css='li[data-id="{}"]'.format(thread_id)).click()

    def perform_search(self, text="dummy"):
        self.q(css=".search-input").fill(text + chr(10))
        self.q(css='btn.btn-small.search-button').click()

    def open_the_post(self, text):
        self.perform_search(text=text)
        self.get_the_thread_id()

    def is_post_deleted(self):
        if not self.q(css='.post-header-content').visible:
            return True
        else:
            raise Exception('The post isnt deleted')


class DiscussionThreadPageExtended(DiscussionsHomePageExtended):

    def __init__(self, browser, course_id, link=''):
        super(DiscussionThreadPageExtended, self).__init__(browser, course_id)
        self.link = link

    @property
    def url(self):
        """
        Construct a URL to the page
        """
        link = self.link.encode('utf-8')
        return link

    def is_browser_on_page(self):
        return self.q(css='.thread-wrapper').visible

    def wait_for_page(self):
        return True

    def get_post_title(self):
        title = self.q(css='h2.post-title')
        return title

    def last_follow_post(self):
        self.q(css='.forum-nav-browse-menu-item.forum-nav-browse-menu-following').click()
        self.wait_for_ajax()
        last_following_post = self.q(css='.forum-nav-thread-title')[0]
        time.sleep(3)
        return last_following_post.text

    def unfollow_post(self):
        follow_star = self.q(css='.btn-link.action-button.action-follow')
        if follow_star.attrs('aria-checked') == [u'true']:
            follow_star.click()
            time.sleep(1)
            self.browser.refresh()
            self.q(css='.forum-nav-browse-menu-item.forum-nav-browse-menu-following').click()
            self.wait_for_ajax()
            titles = self.q(css='.forum-nav-thread-title')
            return titles.text

    def title_header(self):
        self.q(css='.post-title')

    def get_thread_id(self):
        split_link = self.url.split('/')
        return split_link[-1]

    def add_response(self, response):
        split_link = self.url.split('/')
        id = split_link[-1]
        self.q(css='.wmd-input[id="wmd-input-reply-body-{}"]'.format(self.get_thread_id())).fill(response)
        submit = self.q(css='.btn.discussion-submit-post.control-button').click()
        self.wait_for_ajax()

    def edit_post(self, text):
        self.q(css='.btn-link.action-button.action-more').click()
        self.q(css='.btn-link.action-list-item.action-edit').click()
        self.q(css='.edit-post-title.field-input').fill(text)
        self.q(css='#wmd-input-edit-post-body-undefined').fill(text)
        self.q(css='#edit-post-submit').click()

    def edit_response(self, text):
        self.q(css='.response-header-actions .btn-link.action-button.action-more').click()
        self.q(css='.response-header-actions .btn-link.action-list-item.action-edit').click()
        self.q(css='.edit-post-body .wmd-input').fill(text)
        self.q(css='#edit-response-submit').click()

    def edit_comment(self, text):
        self.q(css='.discussion-comment .btn-link.action-button.action-more').click()
        self.q(css='.comment-actions-list .btn-link.action-list-item.action-edit').click()
        self.q(css='.edit-comment-body .wmd-input').fill(text)
        self.q(css='#edit-comment-submit').click()

    def get_response_text(self):
        return self.q(css='.response-body p').text

    def add_comment(self, comment):
        self.q(css='.new-comment').click()
        comment_class = self.q(css='.comment-form')
        comment_id = comment_class.attrs('data-id')
        comment_input =\
           self.q(css='.wmd-input[id="wmd-input-comment-body-{}"]'.format(''.join(comment_id)))

        comment_input.fill(comment)
        submit = self.q(css=".comment-post-control button").click()

    def is_comment_visible(self):
        return self.q(css='.discussion-comment .response-body p').visible

    def get_comment_text(self):
        return self.q(css='.comments .response-body').text

    def delete_comment(self):
        for i in range(2):
            with self.handle_alert():
                self.q(css='.comments button.btn-link.action-button.action-more').click()
                self.q(css='.discussion-comment .btn-link.action-list-item.action-delete').click()
        if self.is_comment_visible():
            raise Exception('Comment isnt deleted')

    def is_comment_deleted(self):
        if not self.q(css='.comments button.btn-link.action-button.action-more').visible:
            return True
        else:
            raise Exception('Comment isnt deleted')

    def delete_response(self):
        with self.handle_alert():
            self.q(css='.response-header-actions .btn-link.action-button.action-more').click()
            self.q(css='.actions-dropdown.is-expanded .btn-link.action-list-item.action-delete').click()

    def is_response_deleted(self):
        if not self.q(css='.response-body p').visible:
            return True
        else:
            raise Exception('Response isnt deleted')

    def delete_post(self):
        with self.handle_alert():
            self.q(css='.post-header-actions .btn-link.action-button.action-more').click()
            self.q(css='.post-header-actions .btn-link.action-list-item.action-delete').click()

            if not self.q(css='.post-header-content').visible:
                return True
            else:
                self.q(css='.post-header-actions .btn-link.action-button.action-more').click()
                self.q(css='.post-header-actions .btn-link.action-list-item.action-delete').click()
