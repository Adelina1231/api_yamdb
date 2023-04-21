from users.models import User


def check_email_exist(email):
    user = User.objects.filter(email=email).first()
    return user is not None


def check_username_exist(username):
    user = User.objects.filter(username=username).first()
    return user is not None
