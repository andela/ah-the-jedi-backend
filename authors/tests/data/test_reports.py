from rest_framework.test import APIClient
from rest_framework import status
from .base_test import BaseTest
from .data import Data
import json
from ...apps.authentication.models import User


class ModelTestCase(BaseTest):
    """
    This class defines the test suite for reports
    """

    def setUp(self):
        """ Define the test client and required test variables. """

        self.client = APIClient()

        self.base_data = Data()

        self.token = self.login_user_and_get_token(self.base_data.user_data)

        self.admin_token = self.login_user_super_user_and_get_token()

        self.control_token = self.login_user_and_get_token(
            self.base_data.user_data2)

    def login_user_and_get_token(self, user={}):

        # signup
        response = self.client.post(
            "/api/users/",
            user,
            format="json"
        )

        # get signup uid and token
        uid, token = response.context['uid'], response.context['token']

        # activate user using token
        self.client.post(
            "/api/users/activate/?uid={}&token={}".format(uid, token),
            format="json"
        )

        # login user using token
        self.client.post(
            "/api/users/",
            user,
            format="json"
        )

        # get token
        res = self.login_user(user)
        return res.data['token']

    def login_user_super_user_and_get_token(self):

        User.objects.create_superuser(
            'SuperUser', 'admin@root.com', 'Admin1211')

        # login user using token
        self.client.post(
            "/api/users/",
            self.base_data.super_user,
            format="json"
        )

        # get token
        res = self.login_user(self.base_data.super_user)

        return res.data['token']

    def create_article(self):
        """
        Function for creating an article
        """

        if not self.control_token:
            self.control_token = self.login_user_and_get_token(
                self.base_data.user_data2)

        article = self.client.post('/api/articles/',
                                   self.base_data.article_data,
                                   HTTP_AUTHORIZATION='Bearer ' +
                                   self.control_token,
                                   format='json')
        return article

    def test_can_create_report(self):
        """
        Test can create a report
        """

        article = self.create_article()
        report = self.base_data.report_data
        report['article'] = article.data['data']['id']

        response = self.client.post('/api/reports/',
                                    report,
                                    HTTP_AUTHORIZATION='Bearer ' +
                                    self.token,
                                    format='json')

        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED)

    def test_cannot_report_for_non_existing_article(self):
        """
        Test cannot create a report for an article that does not exist
        """

        self.create_article()
        report = self.base_data.report_data
        report['article'] = 2000

        response = self.client.post('/api/reports/',
                                    report,
                                    HTTP_AUTHORIZATION='Bearer ' +
                                    self.token,
                                    format='json')

        self.assertEqual(response.status_code,
                         status.HTTP_404_NOT_FOUND)

    def test_cannot_report_own_article(self):
        """
        Test cannot report own article
        """

        article = self.create_article()
        report = self.base_data.report_data
        report['article'] = article.data['data']['id']

        response = self.client.post('/api/reports/',
                                    report,
                                    HTTP_AUTHORIZATION='Bearer ' +
                                    self.control_token,
                                    format='json')

        self.assertEqual(response.status_code,
                         status.HTTP_403_FORBIDDEN)

    def test_cannot_create_duplicate_reports(self):
        """
        Test cannot create duplicate reports
        """

        article = self.create_article()
        report = self.base_data.report_data
        report['article'] = article.data['data']['id']

        self.client.post('/api/reports/',
                         report,
                         HTTP_AUTHORIZATION='Bearer ' +
                         self.control_token,
                         format='json')

        self.client.post('/api/reports/',
                         report,
                         HTTP_AUTHORIZATION='Bearer ' +
                         self.token,
                         format='json')

        response = self.client.post('/api/reports/',
                                    report,
                                    HTTP_AUTHORIZATION='Bearer ' +
                                    self.token,
                                    format='json')

        self.assertEqual(response.status_code,
                         status.HTTP_409_CONFLICT)

    def test_can_get_reports(self):
        """
        Test can get a user's reports
        """

        self.create_article()

        response = self.client.get('/api/reports/',
                                   HTTP_AUTHORIZATION='Bearer ' +
                                   self.control_token,
                                   format='json')

        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)

    def test_cannot_get_non_existing_report(self):
        """
        Test cannot get nonexisting report
        """

        self.create_article()

        response = self.client.get('/api/reports/{}/'.format(2000),
                                   HTTP_AUTHORIZATION='Bearer ' +
                                   self.control_token,
                                   format='json')

        self.assertEqual(response.status_code,
                         status.HTTP_404_NOT_FOUND)

    def test_can_get_one_report(self):
        """
        Test can get one report
        """

        article = self.create_article()

        report = self.base_data.report_data
        report['article'] = article.data['data']['id']

        post_response = self.client.post('/api/reports/',
                                         report,
                                         HTTP_AUTHORIZATION='Bearer ' +
                                         self.token,
                                         format='json')

        report_id = post_response.data['data']['id']

        response = self.client.get('/api/reports/{}/'.format(report_id),
                                   HTTP_AUTHORIZATION='Bearer ' +
                                   self.token,
                                   format='json')

        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)

    def test_cannot_get_report_not_owned_by_user(self):
        """
        Test cannot get a report not reported by the logged in user
        """

        article = self.create_article()

        report = self.base_data.report_data
        report['article'] = article.data['data']['id']

        post_response = self.client.post('/api/reports/',
                                         report,
                                         HTTP_AUTHORIZATION='Bearer ' +
                                         self.token,
                                         format='json')

        report_id = post_response.data['data']['id']

        response = self.client.get('/api/reports/{}/'.format(report_id),
                                   HTTP_AUTHORIZATION='Bearer ' +
                                   self.control_token,
                                   format='json')

        self.assertEqual(response.status_code,
                         status.HTTP_401_UNAUTHORIZED)

    def test_admin_can_get_all_reports(self):
        """
        Test can get all reports
        """

        self.create_article()

        response = self.client.get('/api/report/get_all/',
                                   HTTP_AUTHORIZATION='Bearer ' +
                                   self.admin_token,
                                   format='json')

        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)

    def test_can_update_report(self):
        """
        Test can update a report
        """
        article = self.create_article()

        report = self.base_data.report_data
        report['article'] = article.data['data']['id']

        post_response = self.client.post('/api/reports/',
                                         report,
                                         HTTP_AUTHORIZATION='Bearer ' +
                                         self.token,
                                         format='json')

        report_id = post_response.data['data']['id']
        report['reason'] = "another reason"

        response = self.client.put('/api/reports/{}/'.format(report_id),
                                   report,
                                   HTTP_AUTHORIZATION='Bearer ' +
                                   self.token,
                                   format='json')

        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED)

    def test_cannot_update_report_with_same_reason(self):
        """
        Test cannot update a report with the same reason
        """
        article = self.create_article()

        report = self.base_data.report_data
        report['article'] = article.data['data']['id']

        post_response = self.client.post('/api/reports/',
                                         report,
                                         HTTP_AUTHORIZATION='Bearer ' +
                                         self.token,
                                         format='json')

        report_id = post_response.data['data']['id']

        response = self.client.put('/api/reports/{}/'.format(report_id),
                                   report,
                                   HTTP_AUTHORIZATION='Bearer ' +
                                   self.token,
                                   format='json')

        self.assertEqual(response.status_code,
                         status.HTTP_409_CONFLICT)

    def test_cannot_update_report_not_owned_by_user(self):
        """
        Test cannot update a report that the logged in user does not own
        """
        article = self.create_article()

        report = self.base_data.report_data
        report['article'] = article.data['data']['id']

        post_response = self.client.post('/api/reports/',
                                         report,
                                         HTTP_AUTHORIZATION='Bearer ' +
                                         self.token,
                                         format='json')

        report_id = post_response.data['data']['id']
        report['reason'] = "another reason"

        response = self.client.put('/api/reports/{}/'.format(report_id),
                                   report,
                                   HTTP_AUTHORIZATION='Bearer ' +
                                   self.control_token,
                                   format='json')

        self.assertEqual(response.status_code,
                         status.HTTP_401_UNAUTHORIZED)

    def test_cannot_update_nonexisting_report(self):
        """
        Test cannot update a report that does not exist
        """
        article = self.create_article()

        report = self.base_data.report_data
        report['article'] = article.data['data']['id']

        post_response = self.client.post('/api/reports/',
                                         report,
                                         HTTP_AUTHORIZATION='Bearer ' +
                                         self.token,
                                         format='json')

        report['reason'] = "another reason"

        response = self.client.put('/api/reports/{}/'.format(2000),
                                   report,
                                   HTTP_AUTHORIZATION='Bearer ' +
                                   self.token,
                                   format='json')

        self.assertEqual(response.status_code,
                         status.HTTP_404_NOT_FOUND)

    def test_can_delete_report(self):
        """
        Test can delete a report
        """
        article = self.create_article()

        report = self.base_data.report_data
        report['article'] = article.data['data']['id']

        post_response = self.client.post('/api/reports/',
                                         report,
                                         HTTP_AUTHORIZATION='Bearer ' +
                                         self.token,
                                         format='json')

        report_id = post_response.data['data']['id']

        response = self.client.delete('/api/reports/{}/'.format(report_id),
                                      report,
                                      HTTP_AUTHORIZATION='Bearer ' +
                                      self.token,
                                      format='json')

        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)

    def test_admin_can_delete_report(self):
        """
        Test admin can delete a report
        """
        article = self.create_article()

        report = self.base_data.report_data
        report['article'] = article.data['data']['id']

        post_response = self.client.post('/api/reports/',
                                         report,
                                         HTTP_AUTHORIZATION='Bearer ' +
                                         self.token,
                                         format='json')

        report_id = post_response.data['data']['id']

        response = self.client.delete('/api/report/delete/{}/'.format(report_id),
                                      report,
                                      HTTP_AUTHORIZATION='Bearer ' +
                                      self.admin_token,
                                      format='json')

        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)

    def test_admin_cannot_delete_nonexistin_report(self):
        """
        Test cannot delete non existing report
        """

        article = self.create_article()

        report = self.base_data.report_data
        report['article'] = article.data['data']['id']

        response = self.client.delete('/api/report/delete/{}/'.format(2000),
                                      report,
                                      HTTP_AUTHORIZATION='Bearer ' +
                                      self.admin_token,
                                      format='json')

        self.assertEqual(response.status_code,
                         status.HTTP_404_NOT_FOUND)

    def test_cannot_delete_report_not_owned_by_user(self):
        """
        Test user cannot delete a report they do not own
        """
        article = self.create_article()

        report = self.base_data.report_data
        report['article'] = article.data['data']['id']

        post_response = self.client.post('/api/reports/',
                                         report,
                                         HTTP_AUTHORIZATION='Bearer ' +
                                         self.token,
                                         format='json')

        report_id = post_response.data['data']['id']

        response = self.client.delete('/api/reports/{}/'.format(report_id),
                                      report,
                                      HTTP_AUTHORIZATION='Bearer ' +
                                      self.control_token,
                                      format='json')

        self.assertEqual(response.status_code,
                         status.HTTP_401_UNAUTHORIZED)

    def test_cannot_delete_nonexisting_report(self):
        """
        Test user cannot delete a report they do not own
        """
        article = self.create_article()

        report = self.base_data.report_data
        report['article'] = article.data['data']['id']

        self.client.post('/api/reports/',
                         report,
                         HTTP_AUTHORIZATION='Bearer ' +
                         self.token,
                         format='json')

        response = self.client.delete('/api/reports/{}/'.format(2000),
                                      report,
                                      HTTP_AUTHORIZATION='Bearer ' +
                                      self.token,
                                      format='json')

        self.assertEqual(response.status_code,
                         status.HTTP_404_NOT_FOUND)

    def test_admin_can_delete_article(self):
        """
        Test that admin can delete any article
        """

        article = self.create_article()
        article_slug = article.data['data']['slug']

        response = self.client.delete('/api/articles/delete/{}/'.format(article_slug),
                                      HTTP_AUTHORIZATION='Bearer ' +
                                      self.admin_token,
                                      format='json')

        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)

    def test_admin_cannot_delete_nonexisting_article(self):
        """
        Test that admin cannot delete an article that does not exist
        """

        self.create_article()

        response = self.client.delete('/api/articles/delete/{}/'.format(2000),
                                      HTTP_AUTHORIZATION='Bearer ' +
                                      self.admin_token,
                                      format='json')

        self.assertEqual(response.status_code,
                         status.HTTP_404_NOT_FOUND)
