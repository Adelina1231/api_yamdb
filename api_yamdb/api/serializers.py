from django.shortcuts import get_object_or_404

from rest_framework import serializers
from rest_framework.exceptions import ParseError
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer

from api_yamdb.validators import validate_username
from api_yamdb.settings import LEN_EMAIL, LEN_USERNAME, LEN_TOKEN
from reviews.models import Category, Comment, Genre, Review, Title, User


class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=LEN_EMAIL, allow_blank=False)
    username = serializers.CharField(max_length=LEN_USERNAME,
                                     allow_blank=False,
                                     validators=[validate_username])

    class Meta:
        model = User
        fields = ('email', 'username')


class TokenSerializer(serializers.ModelSerializer):
    confirmation_code = serializers.CharField(allow_blank=False)
    username = serializers.CharField(max_length=LEN_TOKEN,
                                     allow_blank=False,
                                     validators=[validate_username])

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class CategorySerializer(ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(ModelSerializer):
    genre = SlugRelatedField(
        many=True,
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
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )
    title = serializers.SlugRelatedField(
        slug_field='name', read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Review

    def validate(self, data):
        title_id = (
            self.context['request'].parser_context['kwargs']['title_id']
        )
        title = get_object_or_404(Title, pk=title_id)
        user = self.context['request'].user
        if (
            self.context['request'].method == 'POST'
            and Review.objects.filter(author=user, title=title).exists()
        ):
            raise ParseError(
                'Возможен только один отзыв на произведение!'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        exclude = ('review',)
        model = Comment
