"""
Reader statistics tests
"""
import json
from .base_test import BaseTest
from .data import Data


class ReadingStatsTestcase(BaseTest):
    """
    This class defines the test suite for like and dislike
    cases.
    """

    def setUp(self):
        """ Define the test client and required test variables. """

        BaseTest.setUp(self)
        data = self.base_data.user_data2
        signup = self.signup_user()
        signup2 = self.signup_user(data)

        uid = signup.data.get('data')['id']
        token = signup.data.get('data')['token']
        uid_2 = signup2.data.get('data')['id']
        token_2 = signup2.data.get('data')['token']

        self.activate_user(uid=uid, token=token)
        self.activate_user(uid=uid_2, token=token_2)
        self.base_data = Data()

        login = self.login_user()
        self.token = login.data['token']
        self.control_token = self.login_user_and_get_token(data)

    def test_can_add_article_read_count_if_user_authenticated(self):
        """
        Test that a reading count is added after getting
        an article by an authenticated user
        """
        article = self.create_article()
        slug = article.data['data']['slug']

        response = self.client.get('/api/articles/{}/'.format(slug),
                                   HTTP_AUTHORIZATION='Bearer ' +
                                   self.control_token)
        res = json.loads(response.content.decode('utf-8'))

        self.assertEqual(res['data']['read_count'], 1)

    def test_cannot_add_article_read_count_if_user_not_authenticated(self):
        """
        Test that a reading count is not added after getting
        an article by an unauthenticated user
        """
        article = self.create_article()
        slug = article.data['data']['slug']

        self.client.get('/api/articles/{}/'.format(slug))

        # get article as author
        response = self.client.get('/api/articles/{}/'.format(slug),
                                   HTTP_AUTHORIZATION='Bearer ' +
                                   self.token)

        res = json.loads(response.content.decode('utf-8'))

        self.assertEqual(res['data']['read_count'], 0)

    def test_can_get_article_readers_if_owner(self):
        """
        Test that the author can view the people who have
        read the article
        """
        article = self.create_article()
        slug = article.data['data']['slug']

        self.client.get('/api/articles/{}/'.format(slug),
                        HTTP_AUTHORIZATION='Bearer ' +
                        self.control_token)

        response = self.client.get('/api/articles/{}/'.format(slug),
                                   HTTP_AUTHORIZATION='Bearer ' +
                                   self.token)
        res = json.loads(response.content.decode('utf-8'))

        self.assertEqual(res['data']['article_readers'][0], 'NewUser')

    def test_canot_get_article_readers_if_not_owner(self):
        """
        Test that one cannot view the people who have
        read an article if they are not the author
        """
        article = self.create_article()
        slug = article.data['data']['slug']

        response = self.client.get('/api/articles/{}/'.format(slug),
                                   HTTP_AUTHORIZATION='Bearer ' +
                                   self.control_token)
        res = json.loads(response.content.decode('utf-8'))

        self.assertEqual(res['data']['article_readers'], None)
