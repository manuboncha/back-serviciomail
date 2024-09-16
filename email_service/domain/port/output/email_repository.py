from abc import ABC, abstractmethod

from email_service.domain.model.email import Email


class EmailRepository(ABC):

    @abstractmethod
    def save(self, email: Email) -> int:
        pass

    @abstractmethod
    def find_all(self) -> list[Email]:
        pass

    @abstractmethod
    def find_by_id(self, email_id: int) -> Email:
        pass
