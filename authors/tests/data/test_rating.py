"""
Tests for rating an article
"""
import json
from rest_framework import status
from .base_test import BaseTest


class RatingsTest(BaseTest):
    """
    Class defining the test case suite for rating an article
    """

    def setUp(self):
        """ Define the test client and required test variables """

        BaseTest.setUp(self)
        data = self.base_data.user_data2
        user_1, user_2 = self.signup_user(), self.signup_user(data)
        uid, token = user_1.data['data']['id'], user_1.data['data']['token']
        uid_2, token_2 = (user_2.data['data']['id'],
                          user_2.data['data']['token'])
        self.activate_user(uid=uid, token=token)
        self.activate_user(uid=uid_2, token=token_2)
        self.user_token = self.login_user_and_get_token()
        self.control_token = self.login_user_and_get_token(data)
        self.username = self.base_data.user_data["user"]["username"]
        self.control_username = self.base_data.user_data2["user"]["username"]
        self.user_follow = self.follow_user(self.username, self.control_token)

    def create_article(self):
        """
        Method to create an article
        """
        article = self.client.post('/api/articles/',
                                   self.base_data.article_data,
                                   HTTP_AUTHORIZATION='Bearer ' +
                                   self.user_token,
                                   format='json')
        return article

    def test_can_rate_article(self):
        """
        Test a user can rate an article authored by another user
        """
        article = self.create_article()
        slug = article.data['data']['slug']
        rating = self.client.post(
            "/api/articles/{}/rate/".format(slug),
            self.base_data.rating_data,
            format='json',
            HTTP_AUTHORIZATION='Bearer ' + self.control_token
        )

        self.assertEqual(
            rating.status_code,
            status.HTTP_201_CREATED)

        self.assertTrue(
            'Article rating successful' in
            rating.data['message']
        )

    def test_cannot_rate_own_article(self):
        """
        Test a user cannot rate their own article
        """
        article = self.create_article()
        slug = article.data['data']['slug']
        rating = self.client.post(
            "/api/articles/{}/rate/".format(slug),
            self.base_data.rating_data,
            format='json',
            HTTP_AUTHORIZATION='Bearer ' + self.user_token
        )

        self.assertEqual(
            rating.status_code,
            status.HTTP_400_BAD_REQUEST)

        self.assertTrue(
            'You cannot rate your own article' in
            rating.data['errors']['message']
        )

    def test_cannot_rate_an_inexisting_article(self):
        """
        Test a user cannot rate an inexistent article
        """
        slug = 'no-article'
        rating = self.client.post(
            "/api/articles/{}/rate/".format(slug),
            self.base_data.rating_data,
            format='json',
            HTTP_AUTHORIZATION='Bearer ' + self.user_token
        )

        self.assertEqual(
            rating.status_code,
            status.HTTP_400_BAD_REQUEST)

        self.assertTrue(
            'article not found' in
            rating.data['errors']['message']
        )

    def test_average_rating_in_article_details(self):
        """
        Test to ensure that the average rating is returned
        when a user gets an article and that it is a float
        """
        article = self.create_article()
        slug = article.data['data']['slug']

        self.client.post(
            "/api/articles/{}/rate/".format(slug),
            self.base_data.rating_data,
            format='json',
            HTTP_AUTHORIZATION='Bearer ' + self.control_token
        )

        response = self.client.get('/api/articles/{}/'.format(slug))

        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)

        res = json.loads(response.content.decode('utf-8'))
        self.assertTrue('average_rating' in res['data'])
        self.assertIsInstance(res['data']['average_rating'], float)
