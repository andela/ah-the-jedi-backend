from rest_framework import status
from .base_test import BaseTest


class UserTest(BaseTest):
    """
    This class defines the test case suite
    for fetching and manipulating user
    details .
    """

    def setUp(self):
        """ Define the test client and required test variables. """

        BaseTest.setUp(self)

        signup = self.signup_user()

        uid = signup.data.get('data')['id']
        token = signup.data.get('data')['token']

        self.activate_user(uid=uid, token=token)

    def test_successful_fetch_if_authorization_provided(self):
        """
        Tests for successful fetch of current
        authenticated user
        """

        self.client.login(
            username=self.base_data.username,
            password=self.base_data.password
        )

        self.assertEqual(
            self.fetch_current_user().status_code,
            status.HTTP_200_OK
        )

        self.assertTrue(
            self.base_data.user_data["user"]["username"] in
            self.fetch_current_user().data["username"] and
            self.base_data.user_data["user"]["email"] in
            self.fetch_current_user().data["email"]
        )

    def test_successful_update_if_authorization_provided(self):
        """
        Tests for successful update of details if
        current user is authenticated
        """

        self.client.login(
            username=self.base_data.username,
            password=self.base_data.password
        )

        self.assertEqual(
            self.update_user_details().status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            self.update_user_details().data["username"],
            self.base_data.update_data["user"]["username"]
        )

    def test_raises_error_if_authorization_missing(self):
        """
        Test for Forbidden raised if authorization
        not provided
        """

        self.assertEqual(
            self.fetch_current_user().status_code,
            status.HTTP_403_FORBIDDEN
        )

        self.assertTrue(
            "Authentication credentials were not provided" in
            self.fetch_current_user().data["detail"]
        )

    def test_forbidden_error_if_authorization_missing(self):
        """
        Test for Forbidden raised if authorization
        not provided
        """

        self.assertEqual(
            self.update_user_details().status_code,
            status.HTTP_403_FORBIDDEN
        )

        self.assertTrue(
            "Authentication credentials were not provided" in
            self.fetch_current_user().data["detail"]
        )

    def test_raises_error_if_incorrect_authorization_credentials(self):
        """
        Test for Forbidden raised if incorrect
        authorization provided
        """

        self.client.login(
            username=self.base_data.username,
            password="wrongPassword"
        )

        self.assertEqual(
            self.fetch_current_user().status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_raises_forbidden_if_incorrect_authorization_credentials(self):
        """
        Test for Forbidden raised if incorrect
        authorization provided
        """

        self.client.login(
            username=self.base_data.username,
            password="wrongPassword"
        )

        self.assertEqual(
            self.update_user_details().status_code,
            status.HTTP_403_FORBIDDEN
        )
