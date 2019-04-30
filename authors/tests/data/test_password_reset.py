from rest_framework import status
from .base_test import BaseTest


class UserLoginTest(BaseTest):
    """
    Test suite for the user login
    """

    def setUp(self):
        """ Define the test client and required test variables. """

        self.email = {
            "email": 'testuser@email.com',
        }
        self.unregistered_email = {
            "email": "invalid@email.com"
        }
        self.new_pass = {
            "password": "NewTechyPass3"
        }

        self.wrong_pass = {
            "password": "wrong$#$"
        }

        self.invalid_email = {
            "email": "invalid_email"
        }

        BaseTest.setUp(self)

        signup = self.signup_user()
        uid = signup.data.get('id')
        token = signup.data.get('token')

        self.activate_user(uid=uid, token=token)

    def test_successful_email_reset_link_sending(self):
        """
        Tests that a successfully signed up user can
        request password reset link
        """

        data = self.email

        self.response = self.client.post(
            '/api/users/reset_password/',
            data,
            format="json"
        )

        self.assertEqual(self.response.status_code,
                         status.HTTP_200_OK)

    def test_successful_password_reset(self):
        """
        Test that only signed up users can request to reset their passwords
        """

        data = self.email

        self.result = self.client.post(
            '/api/users/reset_password/',
            data,
            format="json"
        )

        token = self.result.data.get('token')
        uid = self.result.data.get('uid')

        self.response = self.client.patch(
            "/api/users/reset_password_confirm/?uid={}&token={}".format(
                uid, token),
            self.new_pass,
            format="json"
        )

        self.assertEqual(self.response.status_code,
                         status.HTTP_200_OK)

    def test_cannot_send_reset_link_to_unregistered_user(self):
        """
        Test that only signed up users can request to reset their passwords
        """
        data = self.unregistered_email

        self.response = self.client.post(
            '/api/users/reset_password/',
            data,
            format="json"
        )

        self.assertEqual(self.response.status_code,
                         status.HTTP_404_NOT_FOUND)

    def test_throws_error_on_empty_email_field(self):
        """
        Test that only signed up users can request to reset their passwords
        """

        data = self.invalid_email

        self.response = self.client.post(
            '/api/users/reset_password/',
            format="json"
        )

        self.assertEqual(self.response.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_throws_error_on_invalid_email_format(self):
        """
        Test that only signed up users can request to reset their passwords
        """
        data = self.invalid_email
        self.response = self.client.post(
            '/api/users/reset_password/',
            data,
            format="json"
        )

        self.assertEqual(self.response.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_throws_error_on_wrong_password_format(self):
        """
        Test that only signed up users can request to reset their passwords
        """

        data = self.email

        self.result = self.client.post(
            '/api/users/reset_password/',
            data,
            format="json"
        )

        token = self.result.data.get('token')
        uid = self.result.data.get('uid')

        self.response = self.client.patch(
            "/api/users/reset_password_confirm/?uid={}&token={}".format(
                uid, token),
            self.wrong_pass,
            format="json"
        )

        self.assertEqual(self.response.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_throws_error_if_password_key_is_missing(self):
        """
        Test that only signed up users can request to reset their passwords
        """

        data = self.email

        self.result = self.client.post(
            '/api/users/reset_password/',
            data,
            format="json"
        )

        token = self.result.data.get('token')
        uid = self.result.data.get('uid')

        self.response = self.client.patch(
            "/api/users/reset_password_confirm/?uid={}&token={}".format(
                uid, token),
            format="json"
        )

        self.assertEqual(self.response.status_code,
                         status.HTTP_400_BAD_REQUEST)
