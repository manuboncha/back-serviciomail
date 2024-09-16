from email_service.domain.exception.email_provider_not_found_config_exception import \
    EmailProviderNotFoundConfigException
from email_service.domain.exception.email_provider_send_email_exception import EmailProviderSendEmailException
from email_service.domain.model.email import Email
from email_service.domain.port.output.email_sender import EmailSender
from email_service.infrastructure.output.email.mailgun_email_provider import MailgunEmailProvider
from email_service.infrastructure.output.email.mailer_send_email_provider import MailSendEmailProvider


class EmailSenderImpl(EmailSender):

    def __init__(self) -> None:
        self.providers = [
            MailSendEmailProvider(),
            MailgunEmailProvider()
        ]

    def send(self, email: Email) -> None:
        last_exception = None
        for provider in self.providers:
            try:
                provider.send(email)
                return
            except (EmailProviderNotFoundConfigException, EmailProviderSendEmailException) as e:
                print(f"Provider {provider.__class__.__name__} failed with error: {e}")
                last_exception = e
        if last_exception:
            print(f"All email providers failed with error: {last_exception}")
