import unittest
from unittest.mock import MagicMock

from email_service.application.use_case.send_email_use_case_impl import SendEmailUseCaseImpl
from email_service.domain.model.email import Email
from email_service.domain.port.output.email_sender import EmailSender


class SendEmailUseCaseImplTests(unittest.TestCase):

    def setUp(self):
        self.mock_email_sender = MagicMock(spec=EmailSender)
        self.send_email_use_case = SendEmailUseCaseImpl(email_sender=self.mock_email_sender)

    def test_send_email_success(self):
        email = Email(id=1, to="test@example.com", subject="Test Subject", body="Test Body")
        self.send_email_use_case.send(email)
        self.mock_email_sender.send.assert_called_once_with(email)

    def test_send_email_failure(self):
        self.mock_email_sender.send.side_effect = Exception("Error sending email")
        email = Email(id=1, to="test@example.com", subject="Test Subject", body="Test Body")
        with self.assertRaises(Exception) as context:
            self.send_email_use_case.send(email)
        self.assertEqual(str(context.exception), "Error sending email")


if __name__ == '__main__':
    unittest.main()
