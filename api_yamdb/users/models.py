from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    ROLES = (
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin')
    )

    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        null=True,
        unique=True
    )
    email = models.EmailField(
        'E-mail',
        unique=True,
        max_length=254,
    )
    role = models.CharField(
        'Роль',
        max_length=50,
        choices=ROLES,
        default=USER
    )
    bio = models.TextField(
        'Биография',
        max_length=200,
        null=True,
        blank=True
    )

    def is_admin(self):
        return self.role == self.ADMIN

    def is_moderator(self):
        return self.role == self.MODERATOR

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
