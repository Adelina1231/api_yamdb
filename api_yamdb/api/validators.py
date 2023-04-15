from rest_framework.exceptions import ValidationError
from reviews.models import User


def validate_username(value):
    if value == 'me':
        raise ValidationError('Недопустимое имя пользователя!')
    elif User.objects.filter(username=value).exists():
        raise ValidationError('Пользователь с таким именем '
                              'уже зарегистрирован')


def validate_email(value):
    if User.objects.filter(email=value).exists():
        raise ValidationError('Пользователь с таким E-mail '
                              'уже зарегистрирован')
