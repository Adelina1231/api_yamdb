from django.core.validators import RegexValidator
from django.utils import timezone
from rest_framework.exceptions import ValidationError


def validate_username(value):
    if value == 'me':
        raise ValidationError('Недопустимое имя пользователя!')


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
