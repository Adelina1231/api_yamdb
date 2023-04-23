from users.models import User


def check_email_exist(email):
    return User.objects.filter(email=email).exists()


def check_username_exist(username):
    return User.objects.filter(username=username).exists()
