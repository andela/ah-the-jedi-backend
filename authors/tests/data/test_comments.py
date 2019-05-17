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


class CommentTestCase(BaseTest):
    """
    This class defines the test suite for create comment
    cases.
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

    def test_a_user_can_create_a_comment(self):
        """
        Test an authenticated user can successfully create a comment
        """
        article = self.create_article()

        slug = article.data['data']['slug']
        comment = self.client.post('/api/articles/{}/comments/'.format(slug),
                                   self.base_data.comment_data,
                                   HTTP_AUTHORIZATION='Bearer ' +
                                   self.token,
                                   format='json')

        self.assertEqual(comment.status_code, 201)

    def test_an_unauthenticated_user_cannot_create_a_comment(self):
        """
        Test an unauthenticated user cannot create a comment
        """
        article = self.create_article()

        slug = article.data['data']['slug']
        comment = self.client.post('/api/articles/{}/comments/'.format(slug),
                                   self.base_data.comment_data,
                                   format='json')

        self.assertEqual(
            comment.data['detail'], "Authentication credentials were not provided.")
        self.assertEqual(comment.status_code, 401)

    def test_create_comment_with_unexisting_slug(self):
        """
        Test a user cannot create a comment with an unexisting article slug
        """
        article = self.create_article()

        comment = self.client.post('/api/articles/{}/comments/'.format("abc"),
                                   self.base_data.comment_data,
                                   HTTP_AUTHORIZATION='Bearer ' +
                                   self.token,
                                   format='json')

        comment = json.loads(comment.content.decode('utf-8'))
        self.assertEqual(comment['error'], 'Article with slug abc not found')
        self.assertEqual(comment['status'], 404)

    def test_cannot_get_comment_with_unexisting_slug(self):
        """
        Test a user cannot get a comment with an unexisting article slug
        """
        article = self.create_article()

        comment = self.client.get('/api/articles/{}/comments/'.format("abc"),
                                  self.base_data.comment_data,
                                  HTTP_AUTHORIZATION='Bearer ' +
                                  self.token,
                                  format='json')

        comment = json.loads(comment.content.decode('utf-8'))
        self.assertEqual(comment['error'], 'Article with slug abc not found')
        self.assertEqual(comment['status'], 404)

    def test_create_comment_on_comment_with_unexisting_parent_id(self):
        """
        Test a user cannot comment on a comment with an unexisting parent id
        """
        article = self.create_article()

        slug = article.data['data']['slug']
        comment = self.client.post('/api/articles/{}/comments/?parent_id=12345'.format(slug),
                                   self.base_data.comment_data,
                                   HTTP_AUTHORIZATION='Bearer ' +
                                   self.token,
                                   format='json')

        comment = json.loads(comment.content.decode('utf-8'))

        self.assertEqual(
            comment['error'], 'No comment with id 12345 found for article with slug first-test-data')
        self.assertEqual(comment['status'], 404)

    def test_get_a_comment_for_article(self):
        """
        Test a user can get a comment for an article
        """
        article = self.create_article()

        slug = article.data['data']['slug']
        self.client.post('/api/articles/{}/comments/'.format(slug),
                         self.base_data.comment_data,
                         HTTP_AUTHORIZATION='Bearer ' +
                         self.token,
                         format='json')

        comments = self.client.get('/api/articles/{}/comments/'.format(slug),
                                   self.base_data.comment_data,
                                   HTTP_AUTHORIZATION='Bearer ' +
                                   self.token,
                                   format='json')

        comments_data = json.loads(comments.content.decode('utf-8'))
        self.assertTrue(comments_data)
        self.assertEqual(comments.status_code, 200)

    def test_get_all_comments_for_article(self):
        """
        Test a user can get all comments for an article
        """
        article = self.create_article()

        slug = article.data['data']['slug']
        self.client.post('/api/articles/{}/comments/'.format(slug),
                         self.base_data.comment_data,
                         HTTP_AUTHORIZATION='Bearer ' +
                         self.token,
                         format='json')
        self.client.post('/api/articles/{}/comments/'.format(slug),
                         self.base_data.comment_data,
                         HTTP_AUTHORIZATION='Bearer ' +
                         self.token,
                         format='json')

        comments = self.client.get('/api/articles/{}/comments/'.format(slug),
                                   self.base_data.comment_data,
                                   HTTP_AUTHORIZATION='Bearer ' +
                                   self.token,
                                   format='json')

        comments_data = json.loads(comments.content.decode('utf-8'))
        self.assertTrue(comments_data)
        self.assertEqual(comments.status_code, 200)

    def test_get_comments_for_article_with_no_comments(self):
        """
        Test a user tries to get comments for an article that has no comment
        """
        article = self.create_article()

        slug = article.data['data']['slug']

        comments = self.client.get('/api/articles/{}/comments/'.format(slug),
                                   self.base_data.comment_data,
                                   HTTP_AUTHORIZATION='Bearer ' +
                                   self.token,
                                   format='json')

        comments_data = json.loads(comments.content.decode('utf-8'))
        self.assertEqual(comments.status_code, 404)

    def test_a_user_can_delete_a_comment(self):
        """
        Test an authenticated user can successfully delete a comment
        """
        article = self.create_article()

        slug = article.data['data']['slug']

        comment = self.create_comment(slug)
        comments_data = json.loads(comment.content.decode('utf-8'))
        id = comments_data['id']

        delete = self.delete_comment(slug, id)

        self.assertEqual(delete.status_code, 200)

    def test_an_unauthenticated_user_cannot_delete_a_comment(self):
        """
        Test an unauthenticated user cannot delete a comment
        """
        article = self.create_article()

        slug = article.data['data']['slug']
        comment = self.create_comment(slug)
        comments_data = json.loads(comment.content.decode('utf-8'))
        id = comments_data['id']

        delete = self.client.delete('/api/articles/{}/comments/?id={}'.format(slug, id),
                                    format='json')

        self.assertEqual(
            delete.data['detail'], "Authentication credentials were not provided.")
        self.assertEqual(delete.status_code, 401)

    def test_delete_comment_with_unexisting_slug(self):
        """
        Test a user cannot delete a comment with an unexisting article slug
        """
        article = self.create_article()

        slug = article.data['data']['slug']
        comment = self.create_comment(slug)
        comments_data = json.loads(comment.content.decode('utf-8'))
        id = comments_data['id']

        delete = self.delete_comment(slug="abc", id=id)

        delete = json.loads(delete.content.decode('utf-8'))
        self.assertEqual(delete['error'], 'Article with slug abc not found')
        self.assertEqual(delete['status'], 404)

    def test_delete_comment_with_unexisting_comment_id(self):
        """
        Test a user cannot delete a comment with an unexisting comment id
        """
        article = self.create_article()

        slug = article.data['data']['slug']
        comment = self.create_comment(slug)
        comments_data = json.loads(comment.content.decode('utf-8'))
        id = comments_data['id']

        delete = self.delete_comment(slug=slug, id=17000)

        delete = json.loads(delete.content.decode('utf-8'))
        self.assertEqual(delete['error'], 'Comment with id 17000 not found')
        self.assertEqual(delete['status'], 404)

    def test_delete_comment_not_owner(self):
        """
        Test cannot delete comment if not owner
        """

        token = self.login_user_and_get_token(self.base_data.user_data2)

        post_response = self.create_article(token=token)
        slug = post_response.data['data']['slug']

        comment = self.create_comment(slug)
        comments_data = json.loads(comment.content.decode('utf-8'))
        id = comments_data['id']

        delete = self.delete_comment(slug=slug, id=id, token=token)

        self.assertEqual(delete.status_code,
                         status.HTTP_403_FORBIDDEN)
