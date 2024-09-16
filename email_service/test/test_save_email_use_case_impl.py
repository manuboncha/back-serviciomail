import unittest
from unittest.mock import MagicMock

from email_service.application.use_case.save_email_use_case_impl import SaveEmailUseCaseImpl
from email_service.domain.model.email import Email
from email_service.infrastructure.output.persistence.email_repository_impl import EmailRepositoryImpl


class SaveEmailUseCaseImplTests(unittest.TestCase):

    def setUp(self):
        self.mock_email_repository = MagicMock(spec=EmailRepositoryImpl)
        self.save_email_use_case = SaveEmailUseCaseImpl(email_repository=self.mock_email_repository)

    def test_save_email_success(self):
        self.mock_email_repository.save.return_value = 1
        email = Email(id=None, to="test@example.com", subject="Test Subject", body="Test Body")
        result = self.save_email_use_case.save(email)
        self.mock_email_repository.save.assert_called_once_with(email)
        self.assertEqual(result, 1)

    def test_save_email_repository_failure(self):
        self.mock_email_repository.save.side_effect = Exception("Error saving email")
        email = Email(id=None, to="test@example.com", subject="Test Subject", body="Test Body")
        with self.assertRaises(Exception) as context:
            self.save_email_use_case.save(email)
        self.assertEqual(str(context.exception), "Error saving email")


if __name__ == '__main__':
    unittest.main()
