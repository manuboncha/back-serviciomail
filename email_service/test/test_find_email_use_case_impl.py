import unittest
from unittest.mock import MagicMock

from email_service.application.use_case.find_email_use_case_impl import FindEmailUseCaseImpl
from email_service.domain.model.email import Email
from email_service.infrastructure.output.persistence.email_repository_impl import EmailRepositoryImpl


class FindEmailUseCaseImplTests(unittest.TestCase):

    def setUp(self):
        self.mock_email_repository = MagicMock(spec=EmailRepositoryImpl)
        self.find_email_use_case = FindEmailUseCaseImpl(email_repository=self.mock_email_repository)

    def test_find_all_emails(self):
        emails = [
            Email(id=1, to="user1@example.com", subject="Subject 1", body="Body 1"),
            Email(id=2, to="user2@example.com", subject="Subject 2", body="Body 2"),
        ]
        self.mock_email_repository.find_all.return_value = emails
        result = self.find_email_use_case.find_all()
        self.mock_email_repository.find_all.assert_called_once()
        self.assertEqual(result, emails)

    def test_find_email_by_id(self):
        email = Email(id=1, to="user1@example.com", subject="Subject 1", body="Body 1")
        self.mock_email_repository.find_by_id.return_value = email
        result = self.find_email_use_case.find_by_id(1)
        self.mock_email_repository.find_by_id.assert_called_once_with(1)
        self.assertEqual(result, email)

    def test_find_email_by_id_not_found(self):
        self.mock_email_repository.find_by_id.return_value = None
        result = self.find_email_use_case.find_by_id(999)
        self.mock_email_repository.find_by_id.assert_called_once_with(999)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
