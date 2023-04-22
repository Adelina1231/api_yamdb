from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models


class User(AbstractUser):
    USER = "user"
    ADMIN = "admin"
    MODERATOR = "moderator"
    ROLES = ((USER, "user"), (MODERATOR, "moderator"), (ADMIN, "admin"))

    role = models.CharField("Роль", max_length=settings.LEN_ROLE,
                            choices=ROLES, default=USER)
    bio = models.TextField("Биография", max_length=settings.LEN_BIO,
                           blank=True)

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_user(self):
        return self.role == self.USER

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
