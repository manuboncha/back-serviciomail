from django.urls import path

from .views import SendEmailView, EmailListView, EmailDetailView

urlpatterns: list[path] = [
    path('v1/emails/send', SendEmailView.as_view(), name='send_email'),
    path('v1/emails', EmailListView.as_view(), name='email_list'),
    path('v1/emails/<int:id>', EmailDetailView.as_view(), name='email_detail'),
]
