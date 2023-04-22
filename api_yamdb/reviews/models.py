from django.db import models
from django.conf import settings

from api_yamdb.validators import validate_year, validate_slug
from users.models import User


class Category(models.Model):
    name = models.CharField(
        'Название',
        max_length=settings.LEN_NAME
    )
    slug = models.SlugField(
        'Адрес',
        max_length=settings.LEN_SLUG,
        validators=(validate_slug,),
        unique=True
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.name[:settings.LEN_TEXT]


class Genre(models.Model):
    name = models.CharField(
        'Название',
        max_length=settings.LEN_NAME
    )
    slug = models.SlugField(
        'Адрес',
        max_length=settings.LEN_SLUG,
        validators=(validate_slug,),
        unique=True
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)

    def __str__(self):
        return self.name[:settings.LEN_TEXT]


class Title(models.Model):
    name = models.CharField(
        'Название',
        max_length=settings.LEN_NAME
    )
    year = models.PositiveIntegerField(
        'Год выпуска',
        db_index=True,
        validators=[validate_year]
    )
    description = models.TextField(
        'Описание',
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        related_name='titles',
        through='GenreTitle'
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('-year', 'name')

    def __str__(self):
        return self.name[:settings.LEN_TEXT]


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='titles')
    genre = models.ForeignKey(
        Genre,
        verbose_name='Жанр',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='genres')

    class Meta:
        verbose_name = 'Произведение и жанр'
        verbose_name_plural = 'Произведения и жанры'
        ordering = ('id',)

    def __str__(self):
        return f'{self.title}, жанр - {self.genre}'


class Review(models.Model):
    text = models.TextField(
        'Текст отзыва',
    )
    score = models.IntegerField(
        'Оценка',
        choices=[(i, i) for i in range(1, settings.LEN_RATING + 1)]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата публикации',
    )
    author = author = models.ForeignKey(
        User,
        on_delete=models.CASCADE, null=True,
        related_name='reviews',
        verbose_name='Автор отзыва',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = (
            models.UniqueConstraint(
                fields=['title', 'author'], name='title_one_review'
            ),
        )
        ordering = ('pub_date',)

    def __str__(self):
        return self.title.name[:settings.LEN_TEXT]


class Comment(models.Model):
    text = models.TextField(
        verbose_name='Комментарий',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата публикации',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE, null=True,
        related_name='comments',
        verbose_name='Автор комментария',
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('pub_date',)
