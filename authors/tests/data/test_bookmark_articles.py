from rest_framework import status
from .base_test import BaseTest
import json


class UserBookmarkArticleTest(BaseTest):
    """
    Test suite for bookmarking an article
    """

    def setUp(self):
        """ Define the test client and required test variables. """

        BaseTest.setUp(self)
        signup = self.signup_user()
        uid = signup.data.get('data')['id']
        token = signup.data.get('data')['token']

        self.activate_user(uid=uid, token=token)
        login = self.login_user()
        self.token = login.data['token']

        signup_user2 = self.signup_user2()
        uid2 = signup_user2.data.get('data')['id']
        token2 = signup_user2.data.get('data')['token']

        self.activate_user(uid=uid2, token=token2)
        login2 = self.login_user2()
        self.token2 = login2.data['token']

        self.article = self.create_article()
        self.slug = self.article.data['data']['slug']

    def test_get_all_bookmarked_articles(self):
        """
        Test user can get all articles he/she has bookmarked
        """
        bookmark_article = self.bookmark_article(
            token=self.token2, slug=self.slug)
        get_bookmarked_articles = self.get_bookmark_article(
            token=self.token2, slug="anyslug")
        self.assertEqual(get_bookmarked_articles.status_code,
                         status.HTTP_200_OK)
        self.assertEqual(len(get_bookmarked_articles.data['data']), 1)

    def test_error_user_cannot_bookmark_own_article(self):
        """
        Tests for error message when user bookmark's own article
        """
        bookmark_article = self.bookmark_article(
            token=self.token, slug=self.slug)

        self.assertEqual(bookmark_article.status_code,
                         status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            bookmark_article.data['error'], "You cannot bookmark your own article")

    def test_successful_bookmark_article(self):
        """
        Test for successful bookmarked article
        """
        bookmark_article = self.bookmark_article(
            token=self.token2, slug=self.slug)

        self.assertEqual(bookmark_article.status_code,
                         status.HTTP_200_OK)
        self.assertEqual(
            bookmark_article.data['data']['author'], 'Alpha')

    def test_successful_unbookmark_article(self):
        """
        Test success message when unbookmarking
        """
        bookmark_article = self.bookmark_article(
            token=self.token2, slug=self.slug)
        unbookmark_article = self.delete_bookmark_article(
            token=self.token2, slug=self.slug)

        self.assertEqual(unbookmark_article.status_code,
                         status.HTTP_200_OK)
        self.assertEqual(
            unbookmark_article.data['data'], "Article unbookmarked successfully")

    def test_article_to_unbookmark_not_found(self):
        """
        Test for error when article not found when unbookmarking
        """

        unbookmark_article = self.delete_bookmark_article(
            token=self.token2, slug="abc")
        self.assertEqual(unbookmark_article.status_code,
                         status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            unbookmark_article.data['error'], "Article with slug abc not found")

    def test_article_to_bookmark_not_found(self):
        """
        Test for error when article not found when bookmarking
        """
        unbookmark_article = self.bookmark_article(
            token=self.token2, slug="abc")
        self.assertEqual(unbookmark_article.status_code,
                         status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            unbookmark_article.data['error'], "Article with slug abc not found")

    def test_article_already_bookmarked(self):
        """
        Test for error when article is already bookmarked
        """

        bookmark_article = self.bookmark_article(self.token2, slug=self.slug)
        bookmark_article2 = self.bookmark_article(self.token2, slug=self.slug)
        self.assertEqual(
            bookmark_article2.data['error'], "You already bookmarked this article")
        self.assertEqual(bookmark_article2.status_code,
                         status.HTTP_400_BAD_REQUEST)
