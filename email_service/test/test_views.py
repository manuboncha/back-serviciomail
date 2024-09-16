from unittest.mock import MagicMock

from django.test import TestCase
from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory, APIClient

from email_service.domain.exception.email_not_found_exception import EmailNotFoundException
from email_service.domain.model.email import Email
from email_service.infrastructure.input.rest.views import EmailListView, EmailDetailView, SendEmailView


class SendEmailViewTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.mock_save_email_use_case = MagicMock()
        self.mock_send_email_use_case = MagicMock()
        self.view = SendEmailView(
            save_email_use_case=self.mock_save_email_use_case,
            send_email_use_case=self.mock_send_email_use_case
        )

    def test_post_save_email_success(self):
        self.mock_save_email_use_case.save.return_value = 1
        request_data = {
            "to": "test@example.com",
            "subject": "Test Subject",
            "body": "Test Body"
        }
        request = self.factory.post('/api/v1/emails/send', request_data, format='json')
        request = Request(request, parsers=[self.view.parser_classes[0]()])
        response = self.view.post(request)
        self.mock_save_email_use_case.save.assert_called_once()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Email sent!')
        self.assertIn('Location', response.headers)
        self.assertTrue(response.headers['Location'].endswith('/api/v1/emails/1'))

    def test_post_save_email_invalid_data(self):
        request_data = {
            "subject": "Test Subject",
            "body": "Test Body"
        }
        request = self.factory.post('/api/v1/emails/send', request_data, format='json')
        request = Request(request, parsers=[self.view.parser_classes[0]()])
        response = self.view.post(request)
        self.mock_save_email_use_case.save.assert_not_called()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class EmailListViewTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.mock_find_email_use_case = MagicMock()
        self.emails = [
            Email(id=1, to="user1@example.com", subject="Subject 1", body="Body 1"),
            Email(id=2, to="user2@example.com", subject="Subject 2", body="Body 2"),
        ]

        self.mock_find_email_use_case.find_all.return_value = self.emails

        self.view = EmailListView(find_email_use_case=self.mock_find_email_use_case)

    def test_get_email_list(self):
        request = self.factory.get('/api/v1/emails')
        response = self.view.get(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(self.emails))
        self.assertEqual(response.data[0]['to'], self.emails[0].to)
        self.assertEqual(response.data[1]['to'], self.emails[1].to)


class EmailDetailViewTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.mock_find_email_use_case = MagicMock()
        self.email = Email(id=1, to="user@example.com", subject="Subject", body="Body")
        self.view = EmailDetailView(find_email_use_case=self.mock_find_email_use_case)

    def test_get_email_detail_success(self):
        self.mock_find_email_use_case.find_by_id.return_value = self.email
        request = self.factory.get('/api/v1/emails/1')
        response = self.view.get(request, id=1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['to'], self.email.to)
        self.assertEqual(response.data['subject'], self.email.subject)

    def test_get_email_detail_not_found(self):
        email_id = 1
        self.mock_find_email_use_case.find_by_id.side_effect = EmailNotFoundException(email_id)
        request = self.factory.get(f'/api/v1/emails/{email_id}/')
        response = self.view.get(request, id=email_id)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], f"Email with ID {email_id} not found.")
