from rest_framework import status
from .base_test import BaseTest


class FollowsTest(BaseTest):
    """
    This class defines the test case suite
    for fetching, following and unfollowing users
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

        uid_2, token_2 = (user_2.data['data']['id'],
                          user_2.data['data']['token'])

        self.activate_user(uid=uid, token=token)

        self.activate_user(uid=uid_2, token=token_2)

        self.user_token = self.login_user_and_get_token()

        self.control_token = self.login_user_and_get_token(data)

        self.username = self.base_data.user_data["user"]["username"]

        self.control_username = self.base_data.user_data2["user"]["username"]

        self.user_follow = self.follow_user(self.username, self.control_token)

    def test_follows_user_successfully(self):
        """
        Test for successful following of a
        user
        """

        user_2 = self.control_username

        follow = self.follow_user(user_2, self.user_token)

        self.assertEqual(follow.status_code, status.HTTP_200_OK)

    def test_unfollows_user_successfully(self):
        """
        Test for successful unfollowing of a
        user
        """

        user_1 = self.username

        unfollow = self.unfollow_user(user_1, self.control_token)

        self.assertEqual(unfollow.status_code, status.HTTP_200_OK)

    def test_fetches_following_successfully(self):
        """
        Test for successful fetch of following users
        """

        user_1 = self.fetch_following(self.control_token)

        self.assertTrue(user_1.status_code, status.HTTP_200_OK)

        self.assertTrue(user_1.data['data']["following"] >= 1)

    def test_fetches_followers_successfully(self):
        """
        Test for successful fetch of user's followers
        """

        user_1 = self.fetch_followers(self.user_token)

        user_2 = self.fetch_followers(self.control_token)

        self.assertTrue(user_1.status_code, status.HTTP_200_OK)

        self.assertTrue(len(user_1.data['data']['users']) >= 1)

        self.assertTrue(user_2.status_code, status.HTTP_200_OK)

        self.assertTrue(user_2.data['data']['followers'] == 0)

    def test_raises_error_if_self_follow(self):
        """
        Test raises Forbidden if users tries to
        follow themselves
        """

        user_1 = self.username

        follow = self.follow_user(user_1, self.user_token)

        self.assertEqual(follow.status_code, status.HTTP_403_FORBIDDEN)

    def test_raises_error_unfollowing_not_followed(self):
        """
        Test raises Bad Request if trying to unfollow
        user not followed
        """

        user_1 = self.username

        follow = self.unfollow_user(user_1, self.user_token)

        self.assertEqual(follow.status_code, status.HTTP_400_BAD_REQUEST)

    def test_raises_error_if_duplicate_follow(self):
        """
        Test raises Forbidden if user attempts to
        duplicate follow request for same user
        """

        follow = self.follow_user(self.username, self.control_token)

        self.assertEqual(follow.status_code, status.HTTP_403_FORBIDDEN)

    def test_raises_fetch_error_if_authentication_missing(self):
        """
        Test raises Unauthorized if authorization not
        provided for fetching user followers and users following
        """

        user_1 = self.fetch_following()

        self.assertTrue(user_1.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_raises_update_error_if_authentication_missing(self):
        """
        Test raises Unauthorized if authorization not provided
        for following or unfollowing a user
        """

        user_1 = self.control_username

        follow = self.follow_user(user_1)

        self.assertEqual(follow.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_raises_error_if_account_missing(self):
        """
        Test raises error if user account does not exist
        """

        follow = self.follow_user("James", self.control_token)

        self.assertEqual(follow.status_code, status.HTTP_404_NOT_FOUND)
