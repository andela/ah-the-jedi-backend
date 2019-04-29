from rest_framework import status
from .base_test import BaseTest


class UserLoginTest(BaseTest):
    """
    Test suite for the user login
    """

    def setUp(self):
        """ Define the test client and required test variables. """

        BaseTest.setUp(self)

        signup = self.signup_user()

        uid = signup.data.get('data')['id']
        token = signup.data.get('data')['token']

        self.activate_user(uid=uid, token=token)

        self.signup_user = self.signup_user(data=self.base_data.user_data2)

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


    def test_user_cannot_login_with_an_inactive_account(self):
        """
        Test method to ensure users cannot login without an inactive
        account
        """

        login = self.login_user(self.base_data.user_data2)

        self.assertEqual(login.status_code,
                         status.HTTP_403_FORBIDDEN)


    def test_user_cannot_activate_account_with_wrong_uid(self):
        """
        Test method to ensure users cannot activate their account with
        a wrong id
        """

        activate = self.activate_user(uid='abc',
                                      token=self.signup_user.data.get('data')['token']
         )

        self.assertEqual(activate.status_code,
                         status.HTTP_400_BAD_REQUEST)

        self.assertEqual(activate.data.get('errors')['uid'][0],
                         'A valid integer is required.')


    def test_user_cannot_activate_account_with_unexisting_uid(self):
        """
        Test method to ensure users cannot activate their account with
        an unexisting id
        """

        activate = self.activate_user(uid='10000',
                                      token=self.signup_user.data.get('data')['token']
         )

        self.assertEqual(activate.status_code,
                         status.HTTP_400_BAD_REQUEST)

        self.assertEqual(activate.data.get('errors')['uid'][0],
                         'Invalid user id, the user does not exist.')


    def test_user_cannot_activate_account_with_wrong_token(self):
        """
        Test method to ensure users cannot activate their account with
        a wrong token
        """

        activate = self.activate_user(uid=self.signup_user.data.get('data')['id'],
                                      token='12345')

        self.assertEqual(activate.status_code,
                         status.HTTP_400_BAD_REQUEST)
        
        self.assertEqual(activate.data.get('errors')['error'][0],
                         'The provided token for the user is not valid.')


    def test_user_can_activate_account_with_right_credentials(self):
        """
        Test method to ensure users can activate their account with
        right credentials
        """

        activate = self.activate_user(uid=self.signup_user.data.get('data')['id'],
                                      token=self.signup_user.data.get('data')['token'])

        self.assertEqual(activate.status_code,200)

        self.assertEqual(activate.data.get('message'),
                         'Your account has been activated.')
