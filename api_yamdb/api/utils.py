from users.models import User
from django.core.exceptions import ObjectDoesNotExist


def check_email_exist(email):
    try:
        User.objects.filter(email=email).first()
        return True
    except ObjectDoesNotExist:
        return False


def check_username_exist(username):
    try:
        return User.objects.filter(username=username).first()
    except ObjectDoesNotExist:
        return False
