from rest_framework.serializers import ModelSerializer
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Genre, Title, GenreTitle


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
