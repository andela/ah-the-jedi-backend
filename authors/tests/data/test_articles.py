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
import json
import os
import random
import string

from PIL import Image


class ModelTestCase(BaseTest):
    """
    This class defines the test suite for create article
    cases.
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

    def test_can_create_article(self, token=''):
        """
        Test can create an article
        """

        if not token:
            token = token = self.login_user_and_get_token(
                self.base_data.user_data)

        response = self.client.post('/api/articles/',
                                    self.base_data.article_data,
                                    HTTP_AUTHORIZATION='Bearer ' +
                                    token,
                                    format='json')

        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED)

    def test_cannot_create_duplicate_article(self, token=''):
        """
        Test can create an article
        """

        if not token:
            token = token = self.login_user_and_get_token(
                self.base_data.user_data)

        self.client.post('/api/articles/',
                         self.base_data.article_data,
                         HTTP_AUTHORIZATION='Bearer ' +
                         token,
                         format='json')

        response = self.client.post('/api/articles/',
                                    self.base_data.article_data,
                                    HTTP_AUTHORIZATION='Bearer ' +
                                    token,
                                    format='json')

        self.assertEqual(response.status_code,
                         status.HTTP_409_CONFLICT)

    def test_can_upload_image(self, token=''):
        """
        Test can create an article
        """

        if not token:
            token = self.login_user_and_get_token(self.base_data.user_data)

        module_dir = os.path.dirname(__file__)
        file_path = os.path.join(module_dir, 'test_files/test.png')
        tempfile = Image.open(file_path)
        image = Image.new('RGB', (100, 100))
        image.save('test.png')

        article = self.base_data.article_data
        article['image'] = tempfile

        response = self.client.post('/api/articles/',
                                    article,
                                    HTTP_AUTHORIZATION='Bearer ' +
                                    token,
                                    format='multipart')

        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED)

    def test_cannot_upload_file_other_than_image(self, token=''):
        """
        Test can create an article
        """

        if not token:
            token = self.login_user_and_get_token(self.base_data.user_data)

        module_dir = os.path.dirname(__file__)
        file_path = os.path.join(module_dir, 'data.py')
        tempfile = open(file_path)

        article = self.base_data.article_data
        article['image'] = tempfile

        response = self.client.post('/api/articles/',
                                    article,
                                    HTTP_AUTHORIZATION='Bearer ' +
                                    token,
                                    format='multipart')

        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_require_missing_fields(self, token=''):
        """
        Test fails to create an article with missing fields
        """

        if not token:
            token = self.login_user_and_get_token(self.base_data.user_data)

        response = self.client.post('/api/articles/',
                                    self.base_data.article_missing_data,
                                    HTTP_AUTHORIZATION='Bearer ' +
                                    token,
                                    format='json')

        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_can_get_all_articles(self, token=''):
        """
        Test can get all articles
        """

        if not token:
            token = self.login_user_and_get_token(self.base_data.user_data)

        self.client.post('/api/articles/',
                         self.base_data.article_data,
                         HTTP_AUTHORIZATION='Bearer ' +
                         token,
                         format='json')

        response = self.client.get('/api/articles/')

        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)

    def test_can_get_all_articles_pagination(self, token=''):
        """
        Test can get all articles has a paginated response
        """

        if not token:
            token = self.login_user_and_get_token(self.base_data.user_data)

        letters = string.ascii_letters
        i = 0
        for i in range(20):
            self.client.post('/api/articles/',
                             self.base_data.article_data,
                             HTTP_AUTHORIZATION='Bearer ' +
                             token,
                             format='json')
            self.base_data.article_data.update({'title': ''.join(random.choice(letters))})
            self.base_data.article_data.update({'body': ''.join(random.choice(letters))})
            i = i+1

        response = self.client.get('/api/articles/')

        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)

        response = json.loads(response.content.decode('utf-8'))

        self.assertEqual(len(response['results']), 9)
        self.assertTrue(response['count'], 19)

    def test_can_get_one_article(self, token=''):
        """
        Test can get all articles
        """

        if not token:
            token = self.login_user_and_get_token(self.base_data.user_data)

        post_response = self.client.post('/api/articles/',
                                         self.base_data.article_data,
                                         HTTP_AUTHORIZATION='Bearer ' +
                                         token,
                                         format='json')

        article_slug = post_response.data['data']['slug']

        response = self.client.get('/api/articles/{}/'.format(article_slug))

        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)

    def test_get_article_not_found(self, token=''):
        """
        Test can get all articles
        """

        if not token:
            token = self.login_user_and_get_token(self.base_data.user_data)

        self.client.post('/api/articles/',
                         self.base_data.article_data,
                         HTTP_AUTHORIZATION='Bearer ' +
                         token,
                         format='json')

        response = self.client.get('/api/articles/{}/'.format(1000))

        self.assertEqual(response.status_code,
                         status.HTTP_404_NOT_FOUND)

    def test_can_update_article(self, token=''):
        """
        Test updates an existing record
        """

        if not token:
            token = self.login_user_and_get_token(self.base_data.user_data)

        response = self.client.post('/api/articles/',
                                    self.base_data.article_data,
                                    HTTP_AUTHORIZATION='Bearer ' +
                                    token,
                                    format='json')

        artcle = json.loads(response.content.decode('utf-8'))
        article_url = artcle['data']['url']

        response = self.client.put(article_url,
                                   self.base_data.article_control_data,
                                   HTTP_AUTHORIZATION='Bearer ' + token,
                                   format='json')
        result = json.loads(response.content.decode('utf-8'))

        self.assertEqual(result['data']['title'], 'Second test data')
        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED)

    def test_update_article_not_found(self, token=''):
        """
        Test updates an existing record
        """

        if not token:
            token = self.login_user_and_get_token(self.base_data.user_data)

        self.client.post('/api/articles/',
                         self.base_data.article_data,
                         HTTP_AUTHORIZATION='Bearer ' +
                         token,
                         format='json')

        response = self.client.put('/api/articles/{}/'.format(1000),
                                   self.base_data.article_control_data,
                                   HTTP_AUTHORIZATION='Bearer ' + token,
                                   format='json')

        self.assertEqual(response.status_code,
                         status.HTTP_404_NOT_FOUND)

    def test_update_article_not_owner(self, token=''):
        """
        Test cannot update article if not owner
        """

        if not token:
            token = self.login_user_and_get_token(self.base_data.user_data)

        post_response = self.client.post('/api/articles/',
                                         self.base_data.article_data,
                                         HTTP_AUTHORIZATION='Bearer ' +
                                         token,
                                         format='json')

        article_slug = post_response.data['data']['slug']

        control_token = self.login_user_and_get_token(
            self.base_data.user_data2)

        response = self.client.put('/api/articles/{}/'.format(article_slug),
                                   self.base_data.article_control_data,
                                   HTTP_AUTHORIZATION='Bearer ' +
                                   control_token,
                                   format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_403_FORBIDDEN)

    def test_can_delete_article(self, token=''):
        """
        Test can delete an article record
        """

        if not token:
            token = self.login_user_and_get_token(self.base_data.user_data)

        post_response = self.client.post('/api/articles/',
                                         self.base_data.article_data,
                                         HTTP_AUTHORIZATION='Bearer ' +
                                         token,
                                         format='json')

        article_slug = post_response.data['data']['slug']

        response = self.client.delete('/api/articles/{}/'.format(article_slug),
                                      HTTP_AUTHORIZATION='Bearer ' +
                                      token,
                                      format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)

    def test_delete_article_not_found(self, token=''):
        """
        Test can delete an article record
        """

        if not token:
            token = self.login_user_and_get_token(self.base_data.user_data)

        self.client.post('/api/articles/',
                         self.base_data.article_data,
                         HTTP_AUTHORIZATION='Bearer ' +
                         token,
                         format='json')

        response = self.client.delete('/api/articles/{}/'.format(1000),
                                      HTTP_AUTHORIZATION='Bearer ' +
                                      token,
                                      format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_404_NOT_FOUND)

    def test_delete_article_not_owner(self, token=''):
        """
        Test cannot delete article if not owner
        """

        if not token:
            token = self.login_user_and_get_token(self.base_data.user_data)

        post_response = self.client.post('/api/articles/',
                                         self.base_data.article_data,
                                         HTTP_AUTHORIZATION='Bearer ' +
                                         token,
                                         format='json')

        article_slug = post_response.data['data']['slug']

        control_token = self.login_user_and_get_token(
            self.base_data.user_data2)

        response = self.client.delete('/api/articles/{}/'.format(article_slug),
                                      HTTP_AUTHORIZATION='Bearer ' +
                                      control_token,
                                      format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_403_FORBIDDEN)
