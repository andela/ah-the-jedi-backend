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

    def test_a_user_can_like_a_comment(self):
        """
        Test an authenticated user can successfully like a comment
        """
        article = self.create_article()

        slug = article.data['data']['slug']
        comment = self.create_comment(slug)
        comment_id = comment.data.get('id')
        like = self.client.post('/api/articles/{}/comments/{}/like/'.format(slug, comment_id),
                                HTTP_AUTHORIZATION='Bearer ' +
                                self.token,
                                format='json')

        self.assertEqual(like.status_code, 200)

    def test_an_unauthenticated_user_cannot_like_a_comment(self):
        """
        Test an unauthenticated user cannot like a comment
        """
        article = self.create_article()

        slug = article.data['data']['slug']
        comment = self.create_comment(slug)
        comment_id = comment.data.get('id')
        like = self.client.post('/api/articles/{}/comments/{}/like/'.format(slug, comment_id),
                                format='json')

        self.assertEqual(
            like.data['detail'], "Authentication credentials were not provided.")
        self.assertEqual(like.status_code, 401)

    def test_cannot_like_comment_with_non_exitent_slug(self):
        """
        Test a user cannot like with an unexisting article slug
        """
        article = self.create_article()

        slug = article.data['data']['slug']
        comment = self.create_comment(slug)
        comment_id = comment.data.get('id')
        like = self.client.post('/api/articles/{}/comments/{}/like/'.format("abc", comment_id),
                                HTTP_AUTHORIZATION='Bearer ' +
                                self.token,
                                format='json')

        like = json.loads(like.content.decode('utf-8'))
        self.assertEqual(like['error'], 'Article with slug abc not found')
        self.assertEqual(int(like['status']), 404)

    def test_cannot_like_comment_with_non_exitent_comment_id(self):
        """
        Test a user cannot like with an unexisting article comment id
        """
        article = self.create_article()

        slug = article.data['data']['slug']
        comment = self.create_comment(slug)
        comment_id = comment.data.get('id')
        like = self.client.post('/api/articles/{}/comments/{}/like/'.format(slug, 70000),
                                HTTP_AUTHORIZATION='Bearer ' +
                                self.token,
                                format='json')

        like = json.loads(like.content.decode('utf-8'))
        self.assertEqual(like['error'], 'Comment with id 70000 not found')
        self.assertEqual(int(like['status']), 404)

    def test_a_user_can_delete_like(self):
        """
        Test an authenticated user can delete a like
        """
        article = self.create_article()

        slug = article.data['data']['slug']
        comment = self.create_comment(slug)
        comment_id = comment.data.get('id')
        self.client.post('/api/articles/{}/comments/{}/like/'.format(slug, comment_id),
                         HTTP_AUTHORIZATION='Bearer ' +
                         self.token,
                         format='json')
        like = self.client.post('/api/articles/{}/comments/{}/like/'.format(slug, comment_id),
                                HTTP_AUTHORIZATION='Bearer ' +
                                self.token,
                                format='json')

        self.assertEqual(like.status_code, 200)

    def test_a_user_can_dislike_a_comment(self):
        """
        Test an authenticated user can successfully disike a comment
        """
        article = self.create_article()

        slug = article.data['data']['slug']
        comment = self.create_comment(slug)
        comment_id = comment.data.get('id')
        dislike = self.client.post('/api/articles/{}/comments/{}/dislike/'.format(slug, comment_id),
                                   HTTP_AUTHORIZATION='Bearer ' +
                                   self.token,
                                   format='json')

        self.assertEqual(dislike.status_code, 200)

    def test_an_unauthenticated_user_cannot_dislike_a_comment(self):
        """
        Test an unauthenticated user cannot dislike a comment
        """
        article = self.create_article()

        slug = article.data['data']['slug']
        comment = self.create_comment(slug)
        comment_id = comment.data.get('id')
        dislike = self.client.post('/api/articles/{}/comments/{}/dislike/'.format(slug, comment_id),
                                   format='json')

        self.assertEqual(
            dislike.data['detail'], "Authentication credentials were not provided.")
        self.assertEqual(dislike.status_code, 401)

    def test_cannot_dislike_comment_with_non_exitent_slug(self):
        """
        Test a user cannot dislike with an unexisting article slug
        """
        article = self.create_article()

        slug = article.data['data']['slug']
        comment = self.create_comment(slug)
        comment_id = comment.data.get('id')
        dislike = self.client.post('/api/articles/{}/comments/{}/dislike/'.format("abc", comment_id),
                                   HTTP_AUTHORIZATION='Bearer ' +
                                   self.token,
                                   format='json')

        dislike = json.loads(dislike.content.decode('utf-8'))
        self.assertEqual(dislike['error'], 'Article with slug abc not found')
        self.assertEqual(int(dislike['status']), 404)

    def test_cannot_dislike_comment_with_non_exitent_comment_id(self):
        """
        Test a user cannot dislike with an unexisting article comment id
        """
        article = self.create_article()

        slug = article.data['data']['slug']
        comment = self.create_comment(slug)
        comment_id = comment.data.get('id')
        dislike = self.client.post('/api/articles/{}/comments/{}/dislike/'.format(slug, 70000),
                                   HTTP_AUTHORIZATION='Bearer ' +
                                   self.token,
                                   format='json')

        dislike = json.loads(dislike.content.decode('utf-8'))
        self.assertEqual(dislike['error'], 'Comment with id 70000 not found')
        self.assertEqual(int(dislike['status']), 404)

    def test_a_user_can_delete_dislike(self):
        """
        Test an authenticated user can delete a dislike
        """
        article = self.create_article()

        slug = article.data['data']['slug']
        comment = self.create_comment(slug)
        comment_id = comment.data.get('id')
        self.client.post('/api/articles/{}/comments/{}/dislike/'.format(slug, comment_id),
                         HTTP_AUTHORIZATION='Bearer ' +
                         self.token,
                         format='json')
        dislike = self.client.post('/api/articles/{}/comments/{}/dislike/'.format(slug, comment_id),
                                   HTTP_AUTHORIZATION='Bearer ' +
                                   self.token,
                                   format='json')

        self.assertEqual(dislike.status_code, 200)
