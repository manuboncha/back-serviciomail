import inject

from email_service.domain.model.email import Email
from email_service.domain.port.input.save_email_use_case import SaveEmailUseCase
from email_service.infrastructure.output.persistence.email_repository_impl import EmailRepositoryImpl


class SaveEmailUseCaseImpl(SaveEmailUseCase):

    @inject.params(email_repository=EmailRepositoryImpl)
    def __init__(self, email_repository: EmailRepositoryImpl) -> None:
        self.email_repository = email_repository

    def save(self, email: Email) -> int:
        return self.email_repository.save(email)
