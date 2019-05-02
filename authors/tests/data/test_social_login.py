from rest_framework import status
from .base_test import BaseTest
from rest_framework.response import Response
import mock
from .data import Data


class SocialLoginTest(BaseTest):
    """
    Test suite for the social login
    """
    def setUp(self):
        """ Define the test client and required test variables. """

        BaseTest.setUp(self)

    def test_successful_social_login_returns_correct_data(self):
        social_user = self.base_data.social_login_data
        with mock.patch('authors.apps.authentication.views.SocialLoginView.post') as mocked_social_login:
            mocked_social_login.return_value = Response({'email': 'kathiekim95@gmail.com', 'username': 'kathrynkate16',
                                                            'token': 'djshjkashdkjashdkjashdks'},
                                                        status=status.HTTP_200_OK)
            response = self.client.post(
                "/api/users/social/login/",
                social_user,
                format="json"
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(
                response.data['email'], "kathiekim95@gmail.com")

    def test_error_message_if_provider_is_invalid(self):
        error_login_user = self.base_data.invalid_provider
        response = self.client.post(
            "/api/users/social/login/",
            error_login_user,
            format="json"
        )
        self.assertEqual(response.status_code,
                            status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['error'], "Provider not supported, Please use 'google-oauth2','facebook', or 'twitter'.")

    def test_successfull_login_with_twitter_returns_correct_data(self):
        twitter_user = self.base_data.twitter_login_data
        with mock.patch('authors.apps.authentication.views.SocialLoginView.post') as mocked_twitter_login:
            mocked_twitter_login.return_value = Response({'email': 'kathiekim95@gmail.com', 'username': 'kathrynkate16'},
                                                            status=status.HTTP_200_OK)
            response = self.client.post(
                "/api/users/social/login/",
                twitter_user,
                format="json"
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(
                response.data['email'], "kathiekim95@gmail.com")

    def test_error_message_if_token_is_invalid(self):
        invalid_login_token = self.base_data.invalid_token
        response = self.client.post(
            "/api/users/social/login/",
            invalid_login_token,
            format="json"
        )
        self.assertEqual(response.status_code,
                            status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['error']['access_token'], 'Invalid token')
