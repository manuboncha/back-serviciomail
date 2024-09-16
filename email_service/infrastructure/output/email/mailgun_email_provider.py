import requests
from decouple import config

from email_service.domain.exception.email_provider_not_found_config_exception import \
    EmailProviderNotFoundConfigException
from email_service.domain.exception.email_provider_send_email_exception import EmailProviderSendEmailException
from email_service.domain.model.email import Email
from email_service.domain.port.output.email_sender import EmailSender


class MailgunEmailProvider(EmailSender):

    def __init__(self):
        self.api_key = config("MAILGUN_API_KEY", default=None)
        self.domain = config("MAILGUN_DOMAIN", default=None)
        if not self.api_key or not self.domain:
            raise EmailProviderNotFoundConfigException("Mailgun")

    def send(self, email: Email) -> None:
        url = f"https://api.mailgun.net/v3/{self.domain}/messages"
        auth = ("api", self.api_key)
        data = {
            "from": "Excited User <mailgun@sandbox8defbdcc8b9b400d847cf4fcbb236237.mailgun.org>",
            "to": [email.to],
            "subject": email.subject,
            "text": email.body
        }
        response = requests.post(url, auth=auth, data=data)
        if response.status_code != 200:
            raise EmailProviderSendEmailException("Mailgun", response.status_code, response.text)
