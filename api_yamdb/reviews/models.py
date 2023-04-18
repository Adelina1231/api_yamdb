from django.db import models
from django.db.models import Avg

from api_yamdb.validators import validate_year, validate_slug
from api_yamdb.settings import LEN_TEXT
from users.models import User

class Category(models.Model):
    name = models.CharField(
        'Название',
        max_length=256,
        db_index=True
    )
    slug = models.SlugField(
        'Адрес',
        max_length=50,
        validators=(validate_slug,),
        unique=True
    )

    def __str__(self):
        return self.name[:LEN_TEXT]

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)


class Genre(models.Model):
    name = models.CharField(
        'Название',
        max_length=256,
        db_index=True
    )
    slug = models.SlugField(
        'Адрес',
        max_length=50,
        validators=(validate_slug,),
        unique=True
    )

    def __str__(self):
        return self.name[:LEN_TEXT]

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)


class Title(models.Model):
    name = models.CharField(
        'Название',
        max_length=256,
        db_index=True
    )
    year = models.IntegerField(
        'Год выпуска',
        validators=[validate_year]
    )
    description = models.TextField(
        'Описание',
        null=True,
        blank=True
    )
    genre = models.ForeignKey(
        Genre,
        verbose_name='Жанр',
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles'
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True
    )

    def __str__(self):
        return self.name[:LEN_TEXT]

    @property
    def rating(self):
        """
        Свойство, возвращающее средний рейтинг произведения, рассчитанный
        на основе всех отзывов.
        """
        reviews = self.reviews.all()
        if reviews:
            return reviews.aggregate(Avg('score'))['score__avg']
        else:
            return None

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE)
    genre = models.ForeignKey(
        Genre,
        verbose_name='Жанр',
        on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}, жанр - {self.genre}'

    class Meta:
        verbose_name = 'Произведение и жанр'
        verbose_name_plural = 'Произведения и жанры'


class Review(models.Model):
    text = models.TextField(
        'Текст отзыва',
    )
    score = models.IntegerField(
        'Оценка',
        choices=[(i, i) for i in range(1, 11)]
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

    def __str__(self):
        return self.title.name

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('pub_date',)


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
