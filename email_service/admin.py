from django.contrib import admin

from email_service.infrastructure.output.persistence.models import EmailModel

admin.site.register(EmailModel)
