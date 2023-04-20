from users.models import User
from django.core.exceptions import ObjectDoesNotExist


def check_email_exist(email):
    try:
        user = User.objects.filter(email=email).first()
        return user is not None
    except ObjectDoesNotExist:
        return False


def check_username_exist(username):
    try:
        user = User.objects.filter(username=username).first()
        return user is not None
    except ObjectDoesNotExist:
        return False
