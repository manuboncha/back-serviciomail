from email_service.domain.exception.email_not_found_exception import EmailNotFoundException
from email_service.domain.model.email import Email
from email_service.domain.port.output.email_repository import EmailRepository
from email_service.domain.serializer.email_serializer import EmailSerializer
from email_service.infrastructure.output.persistence.models import EmailModel


class EmailRepositoryImpl(EmailRepository):

    def save(self, email: Email) -> int:
        email_model = EmailModel.objects.create(to=email.to, subject=email.subject, body=email.body)
        return email_model.id

    def find_by_id(self, email_id: int) -> Email | EmailNotFoundException:
        try:
            email_model = EmailModel.objects.get(id=email_id)
            serializer = EmailSerializer(email_model)
            return serializer.create(serializer.data)
        except EmailModel.DoesNotExist:
            raise EmailNotFoundException(email_id)

    def find_all(self) -> list[Email]:
        email_models = EmailModel.objects.all()
        emails = []
        for email_model in email_models:
            serializer = EmailSerializer(email_model)
            emails.append(serializer.create(serializer.data))
        return emails
