from rest_framework import serializers

from .models import User
from api_yamdb.validators import validate_username


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=254, allow_blank=False)
    username = serializers.CharField(
        max_length=150, allow_blank=False, validators=[validate_username]
    )

    class Meta:
        model = User
        fields = ("email",
                  "username",
                  "first_name",
                  "last_name",
                  "bio",
                  "role")
