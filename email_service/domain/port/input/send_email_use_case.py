from abc import ABC, abstractmethod

from email_service.domain.model.email import Email


class SendEmailUseCase(ABC):

    @abstractmethod
    def send(self, email: Email) -> None:
        pass
