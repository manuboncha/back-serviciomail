from django.db import models


class EmailModel(models.Model):
    to = models.EmailField()
    subject = models.CharField(max_length=255)
    body = models.TextField()
