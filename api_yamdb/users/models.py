from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Roles(models.TextChoices):
        user = 'user', 'Пользователь'
        moderator = 'moderator', 'Модератор'
        admin = 'admin', 'Администратор'
    role = models.CharField(
        max_length=15,
        choices=Roles.choices,
        default=Roles.user
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    email = models.EmailField(
        unique=True
    )

    @property
    def is_admin(self):
        return self.role == self.Roles.admin

    @property
    def is_moderator(self):
        return self.role == self.Roles.moderator

    class Meta:
        ordering = ['id']
