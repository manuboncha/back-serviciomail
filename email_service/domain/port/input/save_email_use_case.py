from abc import ABC, abstractmethod

from email_service.domain.model.email import Email


class SaveEmailUseCase(ABC):

    @abstractmethod
    def save(self, email: Email) -> int:
        pass
