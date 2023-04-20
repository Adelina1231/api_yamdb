from users.models import User
from django.core.exceptions import ObjectDoesNotExist


def check_user_exists(email):
    try:
        user = User.objects.get(email=email)
        return True
    except ObjectDoesNotExist:
        return False
