from rest_framework.serializers import ModelSerializer
from rest_framework.relations import SlugRelatedField
from rest_framework import serializers

from reviews.models import Category, Genre, Title, GenreTitle
from reviews.models import User
from api_yamdb.validators import validate_username


class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=254, allow_blank=False)
    username = serializers.CharField(max_length=150, allow_blank=False,
                                     validators=[validate_username])

    class Meta:
        model = User
        fields = ('email', 'username')


class TokenSerializer(serializers.ModelSerializer):
    confirmation_code = serializers.CharField(allow_blank=False)
    username = serializers.CharField(max_length=150, allow_blank=False,
                                     validators=[validate_username])

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class CategorySerializer(ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Category


class GenreSerializer(ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Genre


class TitleSerializer(ModelSerializer):
    genre = SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all()
    )
    category = SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Title


class GenreTitleSerializer(ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)

    class Meta:
        fields = '__all__'
        model = GenreTitle
