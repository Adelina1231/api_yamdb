import re

from django.core.validators import RegexValidator
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from users.models import User


def validate_username(value):
    error_message = 'Недопустимое имя пользователя!'
    reg = re.compile(r'^[\w.@+-]+$')
    if value == 'me' or not reg.match(value):
        raise ValidationError(error_message)


def validate_username_exist(value):
    if User.objects.filter(username=value).exists():
        raise ValidationError('Пользователь с таким именем '
                              'уже зарегестрирован')


def validate_email(value):
    if User.objects.filter(email=value).exists():
        raise ValidationError('Пользователь с такой почтой '
                              'уже зарегестрирован')


def validate_year(value):
    if value > timezone.now().year:
        raise ValidationError(
            ('Год %(value)s больше текущего!'),
            params={'value': value},
        )


def validate_slug(value):
    value = RegexValidator(regex=r'^[-a-zA-Z0-9_]+$',
                           message='Недопустимый символ в slug')
    return value
