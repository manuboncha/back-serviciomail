import inject

from email_service.domain.model.email import Email
from email_service.domain.port.input.find_email_use_case import FindEmailUseCase
from email_service.infrastructure.output.persistence.email_repository_impl import EmailRepositoryImpl


class FindEmailUseCaseImpl(FindEmailUseCase):

    @inject.params(email_repository=EmailRepositoryImpl)
    def __init__(self, email_repository: EmailRepositoryImpl) -> None:
        self.email_repository = email_repository

    def find_all(self) -> list[Email]:
        return self.email_repository.find_all()

    def find_by_id(self, email_id: int) -> Email:
        return self.email_repository.find_by_id(email_id)
