from rest_framework import status
from .base_test import BaseTest
import json


class UserFavoriteArticleTest(BaseTest):
    """
    Test suite for favoriting an article
    """

    def setUp(self):
        """ Define the test client and required test variables. """

        BaseTest.setUp(self)
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

    def create_article(self):
        """
        Function to create article
        """
        create_article = self.client.post('/api/articles/',
                                          self.base_data.article_data,
                                          HTTP_AUTHORIZATION='Bearer ' +
                                          self.token,
                                          format='json')
        slug = create_article.data['data']['slug']
        return slug

    def test_get_all_favorited_articles(self):
        """
        Test user can get all favorited articles
        """

        favorite_article = self.client.post('/api/articles/{}/favorite/'.
                                            format(self.create_article()),
                                            self.base_data.article_data,
                                            HTTP_AUTHORIZATION='Bearer ' +
                                            self.token2,
                                            format='json')
        get_favorited_articles = self.client.get('/api/articles/{}/favorite/'.
                                                 format("anyslug"),
                                                 self.base_data.article_data,
                                                 HTTP_AUTHORIZATION='Bearer ' +
                                                 self.token2,
                                                 format='json')
        self.assertEqual(get_favorited_articles.status_code,
                         status.HTTP_200_OK)
        self.assertEqual(len(get_favorited_articles.data['data']), 1)

    def test_error_user_cannot_favorite_own_article(self):
        """
        Tests for error message when user favourite's own article
        """
        favorite_article = self.client.post('/api/articles/{}/favorite/'.
                                            format(self.create_article()),
                                            self.base_data.article_data,
                                            HTTP_AUTHORIZATION='Bearer ' +
                                            self.token,
                                            format='json')

        self.assertEqual(favorite_article.status_code,
                         status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            favorite_article.data['error'], "You are not allowed to favourite your own article")

    def test_successful_favorite_article(self):
        """
        Test for successful favorited article
        """

        favorite_article = self.client.post('/api/articles/{}/favorite/'.
                                            format(self.create_article()),
                                            self.base_data.article_data,
                                            HTTP_AUTHORIZATION='Bearer ' +
                                            self.token2,
                                            format='json')

        self.assertEqual(favorite_article.status_code,
                         status.HTTP_200_OK)
        self.assertEqual(
            favorite_article.data['data']['favorited'], True)

    def test_successful_unfavorite_article(self):
        """
        Test success message when unfavoriting
        """

        create_article = self.client.post('/api/articles/',
                                          self.base_data.article_data,
                                          HTTP_AUTHORIZATION='Bearer ' +
                                          self.token,
                                          format='json')
        slug = create_article.data['data']['slug']

        favorite_article = self.client.post('/api/articles/{}/favorite/'.
                                            format(slug),
                                            self.base_data.article_data,
                                            HTTP_AUTHORIZATION='Bearer ' +
                                            self.token2,
                                            format='json')
        unfavorite_article = self.client.delete('/api/articles/{}/favorite/'.
                                                format(slug),
                                                self.base_data.article_data,
                                                HTTP_AUTHORIZATION='Bearer ' +
                                                self.token2,
                                                format='json')

        self.assertEqual(unfavorite_article.status_code,
                         status.HTTP_200_OK)
        self.assertEqual(
            unfavorite_article.data['data'], "Article unfavorited successfully")

    def test_article_to_unfavorite_not_found(self):
        """
        Test for error when article not found when unfavoriting
        """

        unfavorite_article = self.client.delete('/api/articles/{}/favorite/'.
                                                format("abc"),
                                                self.base_data.article_data,
                                                HTTP_AUTHORIZATION='Bearer ' +
                                                self.token2,
                                                format='json')
        self.assertEqual(unfavorite_article.status_code,
                         status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            unfavorite_article.data['error'], "Article with slug abc not found")

    def test_article_to_favorite_not_found(self):
        """
        Test for error when article not found when favoriting
        """

        favorite_article = self.client.post('/api/articles/{}/favorite/'.
                                            format("abc"),
                                            self.base_data.article_data,
                                            HTTP_AUTHORIZATION='Bearer ' +
                                            self.token2,
                                            format='json')
        self.assertEqual(favorite_article.status_code,
                         status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            favorite_article.data['error'], "Article with slug abc not found")

    def test_favorite_false_if_user_is_anonymous(self):
        """
        Test favorited false if user is not authenticated
        """

        create_article = self.client.post('/api/articles/',
                                          self.base_data.article_data,
                                          HTTP_AUTHORIZATION='Bearer ' +
                                          self.token,
                                          format='json')
        slug = create_article.data['data']['slug']

        favorite_article = self.client.post('/api/articles/{}/favorite/'.
                                            format(slug),
                                            self.base_data.article_data,
                                            HTTP_AUTHORIZATION='Bearer ' +
                                            self.token2,
                                            format='json')
        get_article = self.client.get('/api/articles/{}/'.
                                      format(slug),
                                      self.base_data.article_data,
                                      format='json')

        json_data = json.loads(get_article.content.decode('utf-8'))

        self.assertEqual(
            json_data['data']['favorited'], False)
        self.assertEqual(
            json_data['data']['favorites_count'], 1)

    def test_false_if_user_is_logged_in(self):
        """
        Test favorited true if user is logged in
        """

        create_article = self.client.post('/api/articles/',
                                          self.base_data.article_data,
                                          HTTP_AUTHORIZATION='Bearer ' +
                                          self.token,
                                          format='json')
        slug = create_article.data['data']['slug']

        favorite_article = self.client.post('/api/articles/{}/favorite/'.
                                            format(slug),
                                            self.base_data.article_data,
                                            HTTP_AUTHORIZATION='Bearer ' +
                                            self.token2,
                                            format='json')
        get_article = self.client.get('/api/articles/{}/'.
                                      format(slug),
                                      self.base_data.article_data,
                                      HTTP_AUTHORIZATION='Bearer ' +
                                      self.token2,
                                      format='json')

        json_data = json.loads(get_article.content.decode('utf-8'))
        self.assertEqual(
            json_data['data']['favorited'], True)
        self.assertEqual(
            json_data['data']['favorites_count'], 1)

    def test_favorited_is_false_by_default(self):
        """
        Test favorited is false by default
        """

        create_article = self.client.post('/api/articles/',
                                          self.base_data.article_data,
                                          HTTP_AUTHORIZATION='Bearer ' +
                                          self.token,
                                          format='json')
        slug = create_article.data['data']['slug']
        get_article = self.client.get('/api/articles/{}/'.
                                      format(slug),
                                      self.base_data.article_data,
                                      HTTP_AUTHORIZATION='Bearer ' +
                                      self.token2,
                                      format='json')

        json_data = json.loads(get_article.content.decode('utf-8'))
        self.assertEqual(
            json_data['data']['favorited'], False)
