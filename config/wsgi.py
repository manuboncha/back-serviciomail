"""
WSGI config for email_service project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

import inject
from django.core.wsgi import get_wsgi_application

from email_service.injection import configure_injection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

inject.configure(configure_injection)

application = get_wsgi_application()
