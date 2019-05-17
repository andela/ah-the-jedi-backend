from rest_framework import status
from .base_test import BaseTest


class NotificationTest(BaseTest):
    """
    This class defines the test case suite
    for subscribing and unsubscribing to
    email and in-app notifications
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

    def test_creates_in_app_notification_successfully(self):
        """
        Test for successful creation of in app notifications
        if followed user creates an article
        """

        notification = self.fetch_all_notifications(token=self.user_token)

        self.assertEqual(notification.status_code, status.HTTP_200_OK)

        self.assertTrue(notification.data["count"] == 1)

        follow = self.follow_user(self.control_username, self.user_token)

        self.assertEqual(follow.status_code, status.HTTP_200_OK)

        article = self.create_article(token=self.control_token)

        self.assertEqual(article.status_code, status.HTTP_201_CREATED)

        notification = self.fetch_all_notifications(token=self.user_token)

        self.assertEqual(notification.status_code, status.HTTP_200_OK)

        self.assertTrue(notification.data["count"] == 2)

    def test_creates_in_app_notification_if_comment(self):
        """
        Test for successful creation of in app notification
        if comment on favorited article
        """

        notification = self.fetch_all_notifications(token=self.user_token)

        self.assertEqual(notification.status_code, status.HTTP_200_OK)

        self.assertTrue(notification.data["count"] == 1)

        article = self.create_article(token=self.control_token)

        self.assertEqual(article.status_code, status.HTTP_201_CREATED)

        slug = article.data["data"].get("slug", None)

        favorite_article = self.client.post('/api/articles/{}/favorite/'.
                                            format(slug),
                                            self.base_data.article_data,
                                            HTTP_AUTHORIZATION='Bearer ' +
                                            self.user_token,
                                            format='json')

        self.assertEqual(favorite_article.status_code, status.HTTP_200_OK)

        comment = self.client.post('/api/articles/{}/comments/'.format(slug),
                                   self.base_data.comment_data,
                                   HTTP_AUTHORIZATION='Bearer ' +
                                   self.control_token,
                                   format='json')

        self.assertEqual(comment.status_code, status.HTTP_201_CREATED)

        notification = self.fetch_all_notifications(token=self.user_token)

        self.assertEqual(notification.status_code, status.HTTP_200_OK)

        self.assertTrue(notification.data["count"] == 2)

    def test_creates_in_app_notifications_for_article_owner_if_commented(self):
        """
        Test successful creation of in-app notification for the article owner
        if users comment on article
        """

        notification = self.fetch_all_notifications(token=self.control_token)

        self.assertEqual(notification.status_code, status.HTTP_200_OK)

        self.assertTrue(
            "do not have any" in notification.data["notifications"])

        article = self.create_article(token=self.control_token)

        self.assertEqual(article.status_code, status.HTTP_201_CREATED)

        slug = article.data["data"].get("slug", None)

        comment = self.client.post('/api/articles/{}/comments/'.format(slug),
                                   self.base_data.comment_data,
                                   HTTP_AUTHORIZATION='Bearer ' +
                                   self.user_token,
                                   format='json')

        self.assertEqual(comment.status_code, status.HTTP_201_CREATED)

        notification = self.fetch_all_notifications(token=self.control_token)

        self.assertEqual(notification.status_code, status.HTTP_200_OK)

        self.assertTrue(notification.data["count"] == 1)

    def test_creates_in_app_notification_if_follow(self):
        """
        Test creates in_app notification if a user follows
        another user
        """

        notification = self.fetch_all_notifications(token=self.user_token)

        self.assertEqual(notification.status_code, status.HTTP_200_OK)

        self.assertTrue(notification.data["count"] == 1)

    def test_does_not_create_in_app_notification_if_owners_comments(self):
        """
        Test failure to create in-app notification if the article owner
        comments on their own article
        """

        notification = self.fetch_all_notifications(token=self.control_token)

        self.assertEqual(notification.status_code, status.HTTP_200_OK)

        self.assertTrue(
            "do not have any" in notification.data["notifications"])

        article = self.create_article(token=self.control_token)

        self.assertEqual(article.status_code, status.HTTP_201_CREATED)

        slug = article.data["data"].get("slug", None)

        comment = self.client.post('/api/articles/{}/comments/'.format(slug),
                                   self.base_data.comment_data,
                                   HTTP_AUTHORIZATION='Bearer ' +
                                   self.control_token,
                                   format='json')

        self.assertEqual(comment.status_code, status.HTTP_201_CREATED)

        notification = self.fetch_all_notifications(token=self.control_token)

        self.assertEqual(notification.status_code, status.HTTP_200_OK)

        self.assertTrue(
            "do not have any" in notification.data["notifications"])

    def test_does_not_create_in_app_notification_if_self_comments(self):
        """
        Test failure to create in-app notification for the user who
        is commenting on an article
        """

        notification = self.fetch_all_notifications(token=self.user_token)

        author_notifications = self.fetch_all_notifications(
            token=self.control_token)

        self.assertEqual(notification.status_code, status.HTTP_200_OK)

        self.assertEqual(author_notifications.status_code, status.HTTP_200_OK)

        self.assertTrue(notification.data["count"] == 1)

        self.assertTrue(
            "do not have any" in author_notifications.data["notifications"])

        article = self.create_article(token=self.control_token)

        self.assertEqual(article.status_code, status.HTTP_201_CREATED)

        slug = article.data["data"].get("slug", None)

        comment = self.client.post('/api/articles/{}/comments/'.format(slug),
                                   self.base_data.comment_data,
                                   HTTP_AUTHORIZATION='Bearer ' +
                                   self.user_token,
                                   format='json')

        self.assertEqual(comment.status_code, status.HTTP_201_CREATED)

        notification = self.fetch_all_notifications(token=self.user_token)

        author_notifications = self.fetch_all_notifications(
            token=self.control_token)

        self.assertEqual(notification.status_code, status.HTTP_200_OK)

        self.assertTrue(author_notifications.data["count"] == 1)

        self.assertTrue(notification.data["count"] == 1)

    def test_fetches_unread_notifications(self):
        """
        Test for successful fetch of unread notifications
        """

        notification = self.fetch_all_notifications(token=self.user_token)

        self.assertEqual(notification.status_code, status.HTTP_200_OK)

        self.assertTrue(notification.data["count"] == 1)

        follow = self.follow_user(self.control_username, self.user_token)

        self.assertEqual(follow.status_code, status.HTTP_200_OK)

        article = self.create_article(token=self.control_token)

        self.assertEqual(article.status_code, status.HTTP_201_CREATED)

        notification = self.fetch_unread_notifications(token=self.user_token)

        self.assertEqual(notification.status_code, status.HTTP_200_OK)

        self.assertTrue(notification.data["count"] == 2)

    def test_reads_and_fetches_read_notifications(self):
        """
        Test for successful reading and fetch of read
        notifications
        """

        notification = self.fetch_all_notifications(token=self.user_token)

        self.assertEqual(notification.status_code, status.HTTP_200_OK)

        self.assertTrue(notification.data["count"] == 1)

        follow = self.follow_user(self.control_username, self.user_token)

        self.assertEqual(follow.status_code, status.HTTP_200_OK)

        article = self.create_article(token=self.control_token)

        self.assertEqual(article.status_code, status.HTTP_201_CREATED)

        notification = self.fetch_all_notifications(token=self.user_token)

        self.assertTrue(notification.data["count"] == 2)

        id = notification.data["notifications"][0].get("id", None)

        read = self.read_notification(id, self.user_token)

        self.assertEqual(read.status_code, status.HTTP_200_OK)

        notification = self.fetch_read_notifications(token=self.user_token)

        self.assertEqual(notification.status_code, status.HTTP_200_OK)

        self.assertTrue(notification.data["count"] == 1)

        notification = self.fetch_unread_notifications(token=self.user_token)

        self.assertEqual(notification.status_code, status.HTTP_200_OK)

        self.assertTrue(notification.data["count"] == 1)

    def test_fetches_subscriptions(self):
        """
        Test successful fetch of subscriptions
        """

        subscriptions = self.fetch_subscriptions(self.user_token)

        self.assertEqual(subscriptions.status_code, status.HTTP_200_OK)

    def test_updates_subscriptions(self):
        """
        Test for successful opt-out
        of subscription types
        """

        subscriptions = self.fetch_subscriptions(self.user_token)

        self.assertEqual(subscriptions.status_code, status.HTTP_200_OK)

        self.assertEqual(subscriptions.data["subscriptions"]["app"], True)

        updated_subscription = self.update_subscriptions(token=self.user_token)

        self.assertEqual(updated_subscription.status_code, status.HTTP_200_OK)

        self.assertEqual(
            updated_subscription.data["subscriptions"]["app"], False)

        notification = self.fetch_all_notifications(token=self.user_token)

        self.assertEqual(notification.status_code, status.HTTP_200_OK)

        self.assertTrue(notification.data["count"] == 1)

        follow = self.follow_user(self.control_username, self.user_token)

        self.assertEqual(follow.status_code, status.HTTP_200_OK)

        article = self.create_article(token=self.control_token)

        self.assertEqual(article.status_code, status.HTTP_201_CREATED)

        notification = self.fetch_unread_notifications(token=self.user_token)

        self.assertEqual(notification.status_code, status.HTTP_200_OK)

        self.assertTrue(notification.data["count"] == 1)

    def test_raises_error_if_reading_articles_not_owned(self):
        """
        Test raises Forbidden if user tries to read other
        users notifications
        """

        notification = self.fetch_all_notifications(token=self.user_token)

        self.assertEqual(notification.status_code, status.HTTP_200_OK)

        self.assertTrue(notification.data["count"] == 1)

        follow = self.follow_user(self.control_username, self.user_token)

        self.assertEqual(follow.status_code, status.HTTP_200_OK)

        article = self.create_article(token=self.control_token)

        self.assertEqual(article.status_code, status.HTTP_201_CREATED)

        notification = self.fetch_all_notifications(token=self.user_token)

        id = notification.data["notifications"][0].get("id", None)

        read = self.read_notification(id, self.control_token)

        self.assertEqual(read.status_code, status.HTTP_403_FORBIDDEN)

    def test_raises_error_if_notification_not_found(self):
        """
        Test raises Not Found if reading
        notification that does not exist
        """

        read = self.read_notification(50000, self.control_token)

        self.assertEqual(read.status_code, status.HTTP_404_NOT_FOUND)
