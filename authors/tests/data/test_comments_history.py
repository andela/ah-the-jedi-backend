from rest_framework import status
from rest_framework.test import APIClient
from .base_test import BaseTest
from .data import Data


class CommentHistoryTestCase(BaseTest):
    """
    This class defines the test suite for testing updating comment
    and comment history cases.
    """

    def setUp(self):
        """ Define the test client and required test variables. """

        self.client = APIClient()

        self.base_data = Data()

        signup = self.signup_user()

        uid = signup.data.get('data')['id']
        token = signup.data.get('data')['token']

        self.activate_user(uid=uid, token=token)

        login = self.login_user()
        self.token = login.data['token']

        signup_user2 = self.signup_user2()
        uid = signup_user2.data.get('data')['id']
        token = signup_user2.data.get('data')['token']

        self.activate_user(uid=uid, token=token)
        login2 = self.login_user2()
        self.token2 = login2.data['token']

    def test_a_user_can_update_a_comment(self):
        """
        Test an authenticated user can successfully update a comment
        """
        article = self.create_article()
        slug = article.data['data']['slug']

        comment = self.client.post('/api/articles/{}/comments/'.format(slug),
                                   self.base_data.comment_data,
                                   HTTP_AUTHORIZATION='Bearer ' +
                                   self.token,
                                   format='json')
        comment_id = comment.data['id']
        update_comment = self.client.put(
            '/api/articles/{}/comments/?id={}'.format(slug, comment_id),
            self.base_data.comment1_data, HTTP_AUTHORIZATION='Bearer ' +
            self.token, format='json')

        self.assertEqual(update_comment.status_code, status.HTTP_200_OK)
        self.assertEqual(
            update_comment.data['data']['comment'], 'update comment')

    def test_a_user_cannot_update_a_comment_with_same_data(self):
        """
        Test an authenticated user cannot update a comment with the same data
        """
        article = self.create_article()
        slug = article.data['data']['slug']

        comment = self.client.post('/api/articles/{}/comments/'.format(slug),
                                   self.base_data.comment_data,
                                   HTTP_AUTHORIZATION='Bearer ' +
                                   self.token,
                                   format='json')
        comment_id = comment.data['id']
        update_comment = self.client.put(
            '/api/articles/{}/comments/?id={}'.format(slug, comment_id),
            self.base_data.comment_data, HTTP_AUTHORIZATION='Bearer ' +
            self.token, format='json')

        self.assertEqual(update_comment.status_code,
                         status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            update_comment.data['error'], 'This is the current comment')

    def test_update_comment_with_unexisting_slug(self):
        """
        Test a user cannot update a comment with an unexisting article slug
        """
        article = self.create_article()
        slug = article.data['data']['slug']

        comment = self.client.post('/api/articles/{}/comments/'.format(slug),
                                   self.base_data.comment_data,
                                   HTTP_AUTHORIZATION='Bearer ' +
                                   self.token,
                                   format='json')
        comment_id = comment.data['id']
        update_comment = self.client.put(
            '/api/articles/{}/comments/?id={}'.format("abc", comment_id),
            self.base_data.comment1_data, HTTP_AUTHORIZATION='Bearer ' +
            self.token, format='json')

        self.assertEqual(update_comment.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_update_comment_without_comment_id(self):
        """
        Test a user cannot update a comment without a comment_id
        """
        article = self.create_article()
        slug = article.data['data']['slug']

        comment = self.client.post('/api/articles/{}/comments/'.format(slug),
                                   self.base_data.comment_data,
                                   HTTP_AUTHORIZATION='Bearer ' +
                                   self.token,
                                   format='json')
        update_comment = self.client.put(
            '/api/articles/{}/comments/?id={}'.format(slug, ""),
            self.base_data.comment1_data, HTTP_AUTHORIZATION='Bearer ' +
            self.token, format='json')

        self.assertEqual(update_comment.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_update_comment_with_comment_id_that_does_not_exist(self):
        """
        Test a user can't update a comment with comment_id that doesn't exist
        """
        article = self.create_article()
        slug = article.data['data']['slug']

        comment = self.client.post('/api/articles/{}/comments/'.format(slug),
                                   self.base_data.comment_data,
                                   HTTP_AUTHORIZATION='Bearer ' +
                                   self.token,
                                   format='json')
        update_comment = self.client.put(
            '/api/articles/{}/comments/?id={}'.format(slug, 23),
            self.base_data.comment1_data, HTTP_AUTHORIZATION='Bearer ' +
            self.token, format='json')

        self.assertEqual(update_comment.status_code,
                         status.HTTP_404_NOT_FOUND)
        self.assertEqual(update_comment.data['error'], "No comment with id "
                         "23 found for article with slug first-test-data")

    def test_a_user_cannot_update_a_comment_they_do_not_own(self):
        """
        Test an authenticated user cannot update a comment they did not own
        """
        article = self.create_article()
        slug = article.data['data']['slug']

        comment = self.client.post('/api/articles/{}/comments/'.format(slug),
                                   self.base_data.comment_data,
                                   HTTP_AUTHORIZATION='Bearer ' +
                                   self.token,
                                   format='json')
        comment_id = comment.data['id']
        update_comment = self.client.put(
            '/api/articles/{}/comments/?id={}'.format(slug, comment_id),
            self.base_data.comment1_data, HTTP_AUTHORIZATION='Bearer ' +
            self.token2, format='json')

        self.assertEqual(update_comment.status_code,
                         status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            update_comment.data['error'],
            'You cannot update a comment you do not own.')

    def test_a_user_can_get_all_edit_history_of_a_comment(self):
        """
        Test an authenticated user can get all edit history of a comment
        """
        article = self.create_article()
        slug = article.data['data']['slug']

        comment = self.client.post('/api/articles/{}/comments/'.format(slug),
                                   self.base_data.comment_data,
                                   HTTP_AUTHORIZATION='Bearer ' +
                                   self.token,
                                   format='json')
        comment_id = comment.data['id']
        update_comment = self.client.put(
            '/api/articles/{}/comments/?id={}'.format(slug, comment_id),
            self.base_data.comment1_data, HTTP_AUTHORIZATION='Bearer ' +
            self.token, format='json')
        get_edit_history = self.client.get(
            '/api/articles/{}/comments/{}/history/'.format(slug, comment_id),
            HTTP_AUTHORIZATION='Bearer ' + self.token2)

        self.assertEqual(get_edit_history.status_code,
                         status.HTTP_200_OK)

    def test_message_when_there_are_no_comments_edit_history(self):
        """
        Test user can get a message when there are no comments edit history
        """
        article = self.create_article()
        slug = article.data['data']['slug']

        comment = self.client.post('/api/articles/{}/comments/'.format(slug),
                                   self.base_data.comment_data,
                                   HTTP_AUTHORIZATION='Bearer ' +
                                   self.token,
                                   format='json')
        comment_id = comment.data['id']
        get_edit_history = self.client.get(
            '/api/articles/{}/comments/{}/history/'.format(slug, comment_id),
            HTTP_AUTHORIZATION='Bearer ' + self.token)

        self.assertEqual(get_edit_history.status_code,
                         status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            get_edit_history.data['message'], 'This comment has not been '
            'edited')
