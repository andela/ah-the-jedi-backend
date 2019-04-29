import jwt
from authors.apps.authentication.models import User
from rest_framework import status
from .base_test import BaseTest
from authors.settings import SECRET_KEY


class ModelTestCase(BaseTest):
    """
    This class defines the test suite for user registration
    cases.
    """

    def setUp(self):
        """ Define the test client and test variables. """

        self.user = User(
            email='lauder@gmail.com',
            username='Lauder',
            password='adminPassw0rd'
        )

    def test_user_model_can_create__user(self):
        old_count = User.objects.count()
        self.user.save()
        new_count = User.objects.count()
        self.assertNotEqual(old_count, new_count)


class SignupUserViewCase(BaseTest):
    """
    Test suite for user registration
    """

    def setUp(self):
        """ Define the test client and required test variables. """

        BaseTest.setUp(self)

    def test_registers_successfully_if_correct_details(self):
        """
        Test for successful creation of user account
        if correct data provided.
        """

        new_user = self.signup_user()
        # print(new_user.data)

        self.assertEqual(
            new_user.status_code,
            status.HTTP_201_CREATED
        )

        self.assertTrue(
            self.base_data.user_data["user"]["username"] in
            new_user.data.get('data')["username"] and
            self.base_data.user_data["user"]["email"] in
            new_user.data.get('data')["email"]
        )

    def test_raises_error_if_details_missing_key_or_value(self):
        """
        Test raises Bad Request if required detail key or value
        is not provided
        """

        missing_email_key = self.signup_user(self.base_data.missing_user_data)

        self.assertEqual(
            missing_email_key.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertTrue(
            "is required" in missing_email_key.data["errors"]["email"][0]
        )

        self.base_data.missing_user_data["user"].update(
            dict(zip(("username", "email"), ("", "newman@email.com"))))

        self.assertEqual(
            self.signup_user(self.base_data.missing_user_data).status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertTrue(
            "may not be blank" in
            self.signup_user(self.base_data.missing_user_data)
            .data["errors"]["username"][0]
        )

    def test_raises_error_if_duplicate_data_provided(self):
        """
        Test raises Bad Request if duplicate data
        is provided
        """

        self.signup_user()

        new_user = self.signup_user()

        self.assertEqual(
            new_user.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertTrue(
            "email already exists" in
            new_user.data["errors"]["email"][0] and
            "username already exists" in
            new_user.data["errors"]["username"][0]
        )
