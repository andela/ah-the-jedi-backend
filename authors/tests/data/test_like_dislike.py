import json
import os
import jwt
from authors.apps.authentication.models import User
from rest_framework import status
from .base_test import BaseTest
from authors.settings import SECRET_KEY
from django.urls import reverse
from rest_framework.test import APIClient
from .data import Data
from ...apps.articles.models import ArticleModel
from ...apps.articles.views import ArticleView


class LikeDislikeTestCase(BaseTest):
    """
    This class defines the test suite for like and dislike
    cases.
    """

    def setUp(self):
        """ Define the test client and required test variables. """

        # self.client = APIClient()

        # self.base_data = Data()
        BaseTest.setUp(self)
        signup = self.signup_user()

        uid = signup.data.get('data')['id']
        token = signup.data.get('data')['token']

        self.activate_user(uid=uid, token=token)

        login = self.login_user()
        self.token = login.data['token']

    def test_a_user_can_like_article(self):
        """
        Test an authenticated user can successfully like an article
        """
        article = self.create_article()

        slug = article.data['data']['slug']
        like = self.client.post('/api/articles/{}/like/'.format(slug),
                                HTTP_AUTHORIZATION='Bearer ' +
                                self.token,
                                format='json')

        self.assertEqual(like.status_code, 200)

    def test_an_unauthenticated_user_cannot_like_article(self):
        """
        Test an unauthenticated user cannot like article
        """
        article = self.create_article()

        slug = article.data['data']['slug']
        like = self.client.post('/api/articles/{}/like/'.format(slug),
                                format='json')

        self.assertEqual(
            like.data['detail'], "Authentication credentials were not provided.")
        self.assertEqual(like.status_code, 401)

    def test_cannot_like_article_with_non_exitent_slug(self):
        """
        Test a user cannot like with an unexisting article slug
        """
        self.create_article()

        like = self.client.post('/api/articles/{}/like/'.format("abc"),
                                HTTP_AUTHORIZATION='Bearer ' +
                                self.token,
                                format='json')

        like = json.loads(like.content.decode('utf-8'))
        self.assertEqual(like['error'], 'Article with slug abc not found')
        self.assertEqual(like['status'], 404)

    def test_a_user_can_delete_like(self):
        """
        Test an authenticated user can delete a like
        """
        article = self.create_article()

        slug = article.data['data']['slug']
        self.client.post('/api/articles/{}/like/'.format(slug),
                         HTTP_AUTHORIZATION='Bearer ' +
                         self.token,
                         format='json')
        like = self.client.post('/api/articles/{}/like/'.format(slug),
                                HTTP_AUTHORIZATION='Bearer ' +
                                self.token,
                                format='json')

        self.assertEqual(like.status_code, 200)

    def test_a_user_can_dislike_an_article(self):
        """
        Test an authenticated user can successfully disike an article
        """
        article = self.create_article()

        slug = article.data['data']['slug']
        dislike = self.client.post('/api/articles/{}/dislike/'.format(slug),
                                   HTTP_AUTHORIZATION='Bearer ' +
                                   self.token,
                                   format='json')

        self.assertEqual(dislike.status_code, 200)

    def test_an_unauthenticated_user_cannot_dislike_article(self):
        """
        Test an unauthenticated user cannot dislike article
        """
        article = self.create_article()

        slug = article.data['data']['slug']
        dislike = self.client.post('/api/articles/{}/dislike/'.format(slug),
                                   format='json')

        self.assertEqual(
            dislike.data['detail'], "Authentication credentials were not provided.")
        self.assertEqual(dislike.status_code, 401)

    def test_cannot_disllike_article_with_non_exitent_slug(self):
        """
        Test a user cannot dislike with an unexisting article slug
        """
        self.create_article()

        dislike = self.client.post('/api/articles/{}/dislike/'.format("abc"),
                                   HTTP_AUTHORIZATION='Bearer ' +
                                   self.token,
                                   format='json')

        dislike = json.loads(dislike.content.decode('utf-8'))
        self.assertEqual(dislike['error'], 'Article with slug abc not found')
        self.assertEqual(dislike['status'], 404)

    def test_a_user_can_delete_dislike(self):
        """
        Test an authenticated user can delete a dislike
        """
        article = self.create_article()

        slug = article.data['data']['slug']
        self.client.post('/api/articles/{}/dislike/'.format(slug),
                         HTTP_AUTHORIZATION='Bearer ' +
                         self.token,
                         format='json')
        dislike = self.client.post('/api/articles/{}/dislike/'.format(slug),
                                   HTTP_AUTHORIZATION='Bearer ' +
                                   self.token,
                                   format='json')

        self.assertEqual(dislike.status_code, 200)
