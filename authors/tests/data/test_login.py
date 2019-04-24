from rest_framework import status
from .base_test import BaseTest


class UserLoginTest(BaseTest):
    """
    Test suite for the user login
    """

    def setUp(self):
        """ Define the test client and required test variables. """

        BaseTest.setUp(self)

        self.signup_user()

    def test_successful_login_if_correct_credentials(self):
        """
        Tests for successful login if correct credentials
        provided
        """

        registered_user = self.login_user()

        self.assertEqual(
            registered_user.status_code,
            status.HTTP_200_OK
        )

        self.assertTrue(
            self.base_data.user_data["user"]["username"] in
            registered_user.data["username"] and
            self.base_data.user_data["user"]["email"] in
            registered_user.data["email"]
        )

    def test_raises_error_if_missing_or_blank_credential(self):
        """
        Test for Bad Request raised if credentials
        not provided
        """

        self.base_data.login_data["user"].update({
            "email": ""
        })

        self.assertEqual(
            self.login_user().status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertTrue(
            "may not be blank" in self.login_user(
            ).data["errors"]["email"][0]
        )

        self.base_data.login_data["user"].pop("password")

        self.assertTrue(
            "is required" in self.login_user(
            ).data["errors"]["password"][0]
        )

    def test_raises_error_if_incorrect_credentials(self):
        """
        Test for Bad Request raised if incorrect credentials
        provided.
        """

        self.base_data.login_data["user"].update({
            "password": "IncorrectPassword"
        })

        self.assertEqual(
            self.login_user().status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertTrue(
            "email and password was not found" in self.login_user(
            ).data["errors"]["error"][0]
        )
