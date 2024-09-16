import inject

from email_service.domain.model.email import Email
from email_service.domain.port.input.send_email_use_case import SendEmailUseCase
from email_service.infrastructure.output.email.email_sender_impl import EmailSenderImpl


class SendEmailUseCaseImpl(SendEmailUseCase):

    @inject.params(email_sender=EmailSenderImpl)
    def __init__(self, email_sender: EmailSenderImpl) -> None:
        self.email_sender = email_sender

    def send(self, email: Email) -> None:
        self.email_sender.send(email)
