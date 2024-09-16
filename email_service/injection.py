from inject import Binder

from email_service.application.use_case.find_email_use_case_impl import FindEmailUseCaseImpl
from email_service.application.use_case.save_email_use_case_impl import SaveEmailUseCaseImpl
from email_service.application.use_case.send_email_use_case_impl import SendEmailUseCaseImpl
from email_service.domain.port.input.find_email_use_case import FindEmailUseCase
from email_service.domain.port.input.save_email_use_case import SaveEmailUseCase
from email_service.domain.port.input.send_email_use_case import SendEmailUseCase
from email_service.domain.port.output.email_repository import EmailRepository
from email_service.domain.port.output.email_sender import EmailSender
from email_service.infrastructure.output.email.email_sender_impl import EmailSenderImpl
from email_service.infrastructure.output.persistence.email_repository_impl import EmailRepositoryImpl


def configure_injection(binder: Binder) -> None:
    binder.bind(FindEmailUseCase, FindEmailUseCaseImpl)
    binder.bind(SaveEmailUseCase, SaveEmailUseCaseImpl)
    binder.bind(SendEmailUseCase, SendEmailUseCaseImpl)
    binder.bind(EmailSender, EmailSenderImpl)
    binder.bind(EmailRepository, EmailRepositoryImpl)
