import json

from decouple import config
from mailersend import emails

from email_service.domain.exception.email_provider_not_found_config_exception import \
    EmailProviderNotFoundConfigException
from email_service.domain.exception.email_provider_send_email_exception import EmailProviderSendEmailException
from email_service.domain.model.email import Email
from email_service.domain.port.output.email_sender import EmailSender


class MailSendEmailProvider(EmailSender):

    def __init__(self) -> None:
        self.api_key = config("MAILERSEND_API_KEY", default=None)
        if not self.api_key:
            raise EmailProviderNotFoundConfigException("MailerSend")

    def send(self, email: Email) -> None:
        mailer = emails.NewEmail(self.api_key)

        mail_from = {
            "name": "trial",
            "email": "trial@trial-z3m5jgrrzdzgdpyo.mlsender.net",
        }
        recipients = [
            {
                "name": "name",
                "email": email.to,
            }
        ]
        mail_body = {}

        mailer.set_mail_from(mail_from, mail_body)
        mailer.set_mail_to(recipients, mail_body)
        mailer.set_subject(email.subject, mail_body)
        mailer.set_plaintext_content(email.body, mail_body)

        response = mailer.send(mail_body)
        status_code, response_text = response.split('\n', 1)
        status_code = int(status_code.strip())

        if status_code != 202:
            error_data = json.loads(response_text)
            error_message = error_data.get('message', '')
            raise EmailProviderSendEmailException("MailerSend", status_code, error_message)
