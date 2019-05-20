from rest_framework.test import APIClient
from rest_framework import status
from .base_test import BaseTest
from .data import Data
import json


class ModelTestCase(BaseTest):
    """
    This class defines the test suite for search and filter of articles
    """

    def setUp(self):
        """ Define the test client and required test variables. """

        self.client = APIClient()

        self.base_data = Data()

    def login_user_and_get_token(self, user={}):

        # signup
        response = self.client.post(
            "/api/users/",
            user,
            format="json"
        )

        # get signup uid and token
        uid, token = response.context['uid'], response.context['token']

        # activate user using token
        self.client.post(
            "/api/users/activate/?uid={}&token={}".format(uid, token),
            format="json"
        )

        # login user using token
        self.client.post(
            "/api/users/",
            user,
            format="json"
        )

        # get token
        res = self.login_user(user)
        return res.data['token']

    def test_can_filter_by_title(self, token=''):
        """
        Test can filter articles by title
        """

        if not token:
            token = self.login_user_and_get_token(
                self.base_data.user_data)

        post_response = self.client.post('/api/articles/',
                                         self.base_data.article_data,
                                         HTTP_AUTHORIZATION='Bearer ' +
                                         token,
                                         format='json')

        article = json.loads(post_response.content.decode('utf-8'))
        to_look_up = article['data']['title']

        response = self.client.get(
            '/api/article/search/?title=' + to_look_up)

        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)

    def test_can_filter_by_author(self, token=''):
        """
        Test can filter articles by author
        """

        if not token:
            token = self.login_user_and_get_token(
                self.base_data.user_data)

        post_response = self.client.post('/api/articles/',
                                         self.base_data.article_data,
                                         HTTP_AUTHORIZATION='Bearer ' +
                                         token,
                                         format='json')

        article = json.loads(post_response.content.decode('utf-8'))
        to_look_up = article['data']['author']['username']

        response = self.client.get(
            '/api/article/search/?author=' + to_look_up)

        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)

    def test_can_filter_by_tag(self, token=''):
        """
        Test can filter articles by tag
        """

        if not token:
            token = self.login_user_and_get_token(
                self.base_data.user_data)

        data = self.base_data.article_data
        data['tag_list'] = ['testTag']

        self.client.post('/api/articles/',
                         data,
                         HTTP_AUTHORIZATION='Bearer ' +
                         token,
                         format='json')

        response = self.client.get(
            '/api/article/search/?tag=' + 'testTag')

        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)

    def test_can_search_by_title(self, token=''):
        """
        Test can search articles by title
        """

        if not token:
            token = self.login_user_and_get_token(
                self.base_data.user_data)

        post_response = self.client.post('/api/articles/',
                                         self.base_data.article_data,
                                         HTTP_AUTHORIZATION='Bearer ' +
                                         token,
                                         format='json')

        article = json.loads(post_response.content.decode('utf-8'))
        to_look_up = article['data']['title']

        response = self.client.get(
            '/api/article/search/?search=' + to_look_up)

        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)

    def test_can_search_by_author(self, token=''):
        """
        Test can search articles by author
        """

        if not token:
            token = self.login_user_and_get_token(
                self.base_data.user_data)

        post_response = self.client.post('/api/articles/',
                                         self.base_data.article_data,
                                         HTTP_AUTHORIZATION='Bearer ' +
                                         token,
                                         format='json')

        article = json.loads(post_response.content.decode('utf-8'))
        to_look_up = article['data']['author']['username']

        response = self.client.get(
            '/api/article/search/?search=' + to_look_up)

        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)

    def test_can_search_by_body(self, token=''):
        """
        Test can search articles by body
        """

        if not token:
            token = self.login_user_and_get_token(
                self.base_data.user_data)

        post_response = self.client.post('/api/articles/',
                                         self.base_data.article_data,
                                         HTTP_AUTHORIZATION='Bearer ' +
                                         token,
                                         format='json')

        article = json.loads(post_response.content.decode('utf-8'))
        to_look_up = article['data']['body']

        response = self.client.get(
            '/api/article/search/?search=' + to_look_up)

        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)

    def test_can_search_by_description(self, token=''):
        """
        Test can search articles by description
        """

        if not token:
            token = self.login_user_and_get_token(
                self.base_data.user_data)

        post_response = self.client.post('/api/articles/',
                                         self.base_data.article_data,
                                         HTTP_AUTHORIZATION='Bearer ' +
                                         token,
                                         format='json')

        article = json.loads(post_response.content.decode('utf-8'))
        to_look_up = article['data']['description']

        response = self.client.get(
            '/api/article/search/?search=' + to_look_up)

        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)

    def test_can_search_not_found(self, token=''):
        """
        Test can search not found
        """

        if not token:
            token = self.login_user_and_get_token(
                self.base_data.user_data)

        self.client.post('/api/articles/',
                         self.base_data.article_data,
                         HTTP_AUTHORIZATION='Bearer ' +
                         token,
                         format='json')

        response = self.client.get(
            '/api/article/search/?title=' + 'hasgdSUDHjwq,bqkwjhdvkJ')

        self.assertEqual(response.status_code,
                         status.HTTP_404_NOT_FOUND)
