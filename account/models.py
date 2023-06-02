from django.db import models
from reports.models import CompanyData
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    company = models.ForeignKey(CompanyData, on_delete=models.PROTECT, null=True, related_name='users')
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        related_name='user_set_custom'
    )
    groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        related_name='user_set_custom'
    )