from django.contrib.auth.models import AbstractUser
from django.db import models

CHOICES = (
    ('user', 'USER'),
    ('moderator', 'MODERATOR'),
    ('admin', 'ADMIN')
)


class User(AbstractUser):
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )

    role = models.CharField(
        max_length=20,
        verbose_name='Роль',
        default='user',
        choices=CHOICES,
    )
