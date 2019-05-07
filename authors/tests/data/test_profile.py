from rest_framework import status
from .base_test import BaseTest
from django.core.files.uploadedfile import SimpleUploadedFile


class ProfileTest(BaseTest):
    """
    This class defines the test case suite
    for fetching and manipulating user
    profiles.
    """

    def setUp(self):
        """
        Define the test client and required
        test variables.
        """

        BaseTest.setUp(self)

        data = self.base_data.user_data2

        user_1, user_2 = self.signup_user(), self.signup_user(data)

        uid, token = user_1.data['data']['id'], user_1.data['data']['token']

        uid_2, token_2 = user_2.data['data']['id'], user_2.data['data']['token']

        self.activate_user(uid=uid, token=token)

        self.activate_user(uid=uid_2, token=token_2)

        self.user_token = self.login_user_and_get_token()

        self.username = self.base_data.user_data["user"]["username"]

        self.control_username = self.base_data.user_data2["user"]["username"]

    def test_successful_profile_creation_on_signup(self):
        """
        Test for successful creation of a user's
        profile on account creation.
        """

        username = self.base_data.user_data["user"].get("username", '')

        user_profile = self.fetch_user_profile(username)

        self.assertEqual(user_profile.status_code,
                         status.HTTP_200_OK)

        self.assertNotEqual(user_profile.status_code,
                            status.HTTP_404_NOT_FOUND)

        self.assertTrue(username in
                        user_profile.data["username"])

    def test_raises_not_found_if_missing_profile(self):
        """
        Test raises Not Found if user profile does not
        exist.
        """

        profile = self.fetch_user_profile("alphanso")

        self.assertEqual(profile.status_code,
                         status.HTTP_404_NOT_FOUND)

        self.assertTrue("does not exist" in profile.data["errors"])

    def test_updates_profile_if_authorized_valid_data(self):
        """
        Test for successful update of user profile
        if authorization and correct payload provided
        """

        updated_profile = self.update_user_profile(
            username=self.username, token=self.user_token)

        self.assertEqual(updated_profile.status_code,
                         status.HTTP_200_OK)

        self.assertEqual(updated_profile.data["bio"],
                         self.base_data.profile_data["bio"])

    def test_updates_profile_if_image_provided(self):
        """
        Test for successful update of user profile
        if authorization and image provided within
        the payload
        """

        updated_profile = self.update_user_profile(
            username=self.username,
            token=self.user_token,
            image=self.generate_image())

        self.assertEqual(updated_profile.status_code,
                         status.HTTP_200_OK)

    def test_raises_unauthorized_if_token_not_provided(self):
        """
        Test raises Unauthorized if authentication
        incorrect or not provided.
        """

        updated_profile = self.update_user_profile(
            username=self.username)

        self.assertEqual(updated_profile.status_code,
                         status.HTTP_401_UNAUTHORIZED)

    def test_raises_forbidden_if_not_profile_owner(self):
        """
        Test raises Forbidden if updating a profile
        the user does not own.
        """

        updated_profile = self.update_user_profile(
            username=self.control_username, token=self.user_token)

        self.assertEqual(updated_profile.status_code,
                         status.HTTP_403_FORBIDDEN)

    def test_raises_bad_request_if_file_not_image(self):
        """
        Test raises Bad Request if image in payload
        populated with none-image file.
        """

        image = SimpleUploadedFile("document.pdf",
                                   b"file_content",
                                   content_type="document/pdf")

        updated_profile = self.update_user_profile(
            username=self.username,
            token=self.user_token,
            image=image)

        self.assertEqual(updated_profile.status_code,
                         status.HTTP_400_BAD_REQUEST)

        self.assertTrue(
            "Ensure that the file is an image" in
            updated_profile.data["errors"])

    def test_authenticated_user_gets_all_profiles(self):
        """
        Test that shows an authenticated user can get all listed user profiles.
        """
        profiles = self.get_all_profiles(token=self.user_token)

        self.assertEqual(profiles.status_code, 200)
        self.assertTrue(profiles.data)

    def test_unauthenticated_user_cannot_get_all_profiles(self):
        """
        Test that shows an unauthenticated user cannot get all listed user profiles.
        """
        profiles = self.get_all_profiles(token='')

        self.assertEqual(profiles.status_code, 401)
