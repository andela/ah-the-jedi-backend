from django.test import TestCase
from rest_framework.test import APIClient
from .data import Data


class BaseTest(TestCase):
    """
    This class 'BaseTest', contains setup used by
    all other tests
    """

    def setUp(self):
        """ Define the test client and required test variables. """

        self.client = APIClient()

        self.base_data = Data()

    def signup_user(self, data=''):
        """
        This method 'signup_user' creates an account
        using the provided details
        """

        data = data or self.base_data.user_data

        return self.client.post(
            "/api/users/",
            data,
            format="json"
        )

    def activate_user(self, uid, token):
        """
        This method 'activate_user' activates a user account
        using the provided details
        """

        return self.client.post(
            "/api/users/activate/?uid={}&token={}".format(uid, token),
            format="json"
        )

    def login_user(self, data=''):
        """
        This method 'login_user'
        attempts to log in a user
        with the data provided
        """

        data = data or self.base_data.login_data

        response = self.client.post(
            "/api/users/login/",
            data,
            format="json"
        )

        return response

    def fetch_current_user(self, headers=None):
        """
        This method 'fetch_current_user'
        fetches details of current user
        provided with correct authorization
        """
        if headers:
            return self.client.get(
                "/api/user/",
                format="json",
                HTTP_AUTHORIZATION='Bearer ' + headers
            )

        else:
            return self.client.get(
                "/api/user/",
                format="json"
            )

    def update_user_details(self, data='', token=None):
        """
        This method 'update_user_details'
        updates details of current user with
        the provided data
        """

        data = data or self.base_data.update_data

        if token:
            return self.client.put(
                "/api/user/",
                data,
                format="json",
                HTTP_AUTHORIZATION='Bearer ' + token
            )
        else:
            return self.client.put(
                "/api/user/",
                data,
                format="json"
            )

    def login_user_and_get_token(self):
        res = self.login_user()
        token = res.data['token']

        return token
