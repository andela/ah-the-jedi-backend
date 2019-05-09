import json
from rest_framework import status
from .base_test import BaseTest
from .data import Data


class HighlightArticleTestcase(BaseTest):
    """
    This class defines the test suite for like and dislike
    cases.
    """

    def setUp(self):
        """ Define the test client and required test variables. """

        BaseTest.setUp(self)
        signup = self.signup_user()

        uid = signup.data.get('data')['id']
        token = signup.data.get('data')['token']

        self.activate_user(uid=uid, token=token)
        self.base_data = Data()

        login = self.login_user()
        self.token = login.data['token']

    def test_a_user_can_highlight_article_body(self):
        """
        Test an authenticated user can successfully highlight an article
        """
        article = self.create_article()

        slug = article.data['data']['slug']
        highlight = self.client.post('/api/articles/{}/highlight/'.format(slug),
                                     self.base_data.highlight_data,
                                     HTTP_AUTHORIZATION='Bearer ' +
                                     self.token,
                                     format='json')

        self.assertEqual(highlight.status_code, 200)

    def test_an_unauthenticated_user_cannot_highlight_article(self):
        """
        Test an unauthenticated user cannot highlight article
        """
        article = self.create_article()

        slug = article.data['data']['slug']
        highlight = self.client.post('/api/articles/{}/highlight/'.format(slug),
                                     self.base_data.highlight_data,
                                     format='json')

        self.assertEqual(highlight.status_code, 401)

    def test_cannot_highlight_article_with_non_exitent_slug(self):
        """
        Test a user cannot highlight with an unexisting article slug
        """

        highlight = self.client.post('/api/articles/{}/highlight/'.format("abc"),
                                     self.base_data.highlight_data,
                                     HTTP_AUTHORIZATION='Bearer ' +
                                     self.token,
                                     format='json')

        self.assertEqual(highlight.status_code, 404)

    def test_cannot_highlight_inexistent_text_in_an_article(self):
        """
        Test a user cannot highlight with an inexistent text
        """
        article = self.create_article()

        slug = article.data['data']['slug']
        highlight = self.client.post('/api/articles/{}/highlight/'.format(slug),
                                     self.base_data.in_existent_highlight_data,
                                     HTTP_AUTHORIZATION='Bearer ' +
                                     self.token,
                                     format='json')

        self.assertEqual(highlight.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            highlight.data['error'], "The highlighted text is not found in this article body")

    def test_a_user_cannot_highlight_article_more_than_once(self):
        """
        Test an authenticated user cannot highlight article twice
        """
        article = self.create_article()

        slug = article.data['data']['slug']
        self.client.post('/api/articles/{}/highlight/'.format(slug),
                         self.base_data.highlight_data,
                         HTTP_AUTHORIZATION='Bearer ' +
                         self.token,
                         format='json')
        highlight = self.client.post('/api/articles/{}/highlight/'.format(slug),
                                     self.base_data.highlight_data,
                                     HTTP_AUTHORIZATION='Bearer ' +
                                     self.token,
                                     format='json')

        self.assertEqual(highlight.status_code, 409)

    def test_a_user_can_highlight_article_title(self):
        """
        Test an authenticated user can successfully highlight an article title
        """
        article = self.create_article()

        slug = article.data['data']['slug']
        highlight = self.client.post('/api/articles/{}/highlight/'.format(slug),
                                     self.base_data.highlight_data_title,
                                     HTTP_AUTHORIZATION='Bearer ' +
                                     self.token,
                                     format='json')

        self.assertEqual(highlight.status_code, 200)

    def test_a_user_can_highlight_article_description(self):
        """
        Test an authenticated user can successfully
        highlight an article decription
        """
        article = self.create_article()

        slug = article.data['data']['slug']
        highlight = self.client.post('/api/articles/{}/highlight/'.format(slug),
                                     self.base_data.highlight_data_description,
                                     HTTP_AUTHORIZATION='Bearer ' +
                                     self.token,
                                     format='json')

        self.assertEqual(highlight.status_code, 200)
