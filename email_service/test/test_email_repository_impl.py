import unittest
from unittest.mock import MagicMock, patch

from email_service.domain.exception.email_not_found_exception import EmailNotFoundException
from email_service.domain.model.email import Email
from email_service.infrastructure.output.persistence.email_repository_impl import EmailRepositoryImpl
from email_service.infrastructure.output.persistence.models import EmailModel


class EmailRepositoryImplTests(unittest.TestCase):

    def setUp(self):
        self.email_repository = EmailRepositoryImpl()

    @patch('email_service.infrastructure.output.persistence.models.EmailModel.objects.create')
    def test_save_email_success(self, mock_create):
        mock_create.return_value.id = 1
        email = Email(id=None, to="test@example.com", subject="Test Subject", body="Test Body")
        result = self.email_repository.save(email)
        mock_create.assert_called_once_with(to=email.to, subject=email.subject, body=email.body)
        self.assertEqual(result, 1)

    @patch('email_service.infrastructure.output.persistence.models.EmailModel.objects.get')
    @patch('email_service.domain.serializer.email_serializer.EmailSerializer.__new__')
    def test_find_by_id_success(self, mock_serializer_init, mock_get):
        email_model = MagicMock(spec=EmailModel)
        mock_get.return_value = email_model
        email = Email(id=1, to="test@example.com", subject="Test Subject", body="Test Body")

        mock_serializer = MagicMock()
        mock_serializer.create.return_value = email
        mock_serializer_init.return_value = mock_serializer
        result = self.email_repository.find_by_id(1)
        mock_get.assert_called_once_with(id=1)
        mock_serializer.create.assert_called_once_with(mock_serializer.data)
        self.assertEqual(result, email)

    @patch('email_service.infrastructure.output.persistence.models.EmailModel.objects.get')
    def test_find_by_id_not_found(self, mock_get):
        mock_get.side_effect = EmailModel.DoesNotExist
        with self.assertRaises(EmailNotFoundException) as context:
            self.email_repository.find_by_id(1)
        self.assertEqual(context.exception.email_id, 1)

    @patch('email_service.infrastructure.output.persistence.models.EmailModel.objects.all')
    @patch('email_service.domain.serializer.email_serializer.EmailSerializer.__new__')
    def test_find_all_success(self, mock_serializer_init, mock_all):
        email_models = [MagicMock(spec=EmailModel), MagicMock(spec=EmailModel)]
        mock_all.return_value = email_models
        emails = [
            Email(id=1, to="user1@example.com", subject="Subject 1", body="Body 1"),
            Email(id=2, to="user2@example.com", subject="Subject 2", body="Body 2"),
        ]

        mock_serializer = MagicMock()
        mock_serializer.create.side_effect = emails
        mock_serializer_init.return_value = mock_serializer
        result = self.email_repository.find_all()
        mock_all.assert_called_once()
        self.assertEqual(mock_serializer.create.call_count, len(email_models))
        self.assertEqual(result, emails)


if __name__ == '__main__':
    unittest.main()
