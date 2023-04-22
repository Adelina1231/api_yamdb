from django.conf import settings
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import User
from api_yamdb.validators import (
    validate_username,
    validate_email,
    validate_username_exist,
)


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=settings.LEN_EMAIL,
        allow_blank=False, validators=[validate_email]
    )
    username = serializers.CharField(
        max_length=settings.LEN_USERNAME,
        allow_blank=False,
        validators=[validate_username, validate_username_exist],
    )

    class Meta:
        model = User
        fields = ("email",
                  "username",
                  "first_name",
                  "last_name",
                  "bio",
                  "role")
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(), fields=("username", "email")
            )
        ]
