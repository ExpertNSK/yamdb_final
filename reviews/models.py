from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import UsernameValidator

ADMIN = 'admin'
MODERATOR = 'moderator'
USER = 'user'

ROLE_CHOICES = [
    (USER, 'user'),
    (MODERATOR, 'moderator'),
    (ADMIN, 'administrator'),
]


class User(AbstractUser):
    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        unique=True,
        validators=[UsernameValidator]
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
    )
    email = models.EmailField(
        'Адрес электронной почты',
        max_length=254,
        unique=True,
        blank=False,
    )
    role = models.CharField(
        'Роль',
        max_length=max(len(role[1]) for role in ROLE_CHOICES),
        choices=ROLE_CHOICES,
        default=USER
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )

    @property
    def is_admin(self):
        return (
            self.role == ADMIN
            or self.is_superuser
            or self.is_staff
        )

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('id',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('id',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.TextField()
    year = models.IntegerField(
        verbose_name='Дата выхода',
        validators=[
            MinValueValidator(0),
            MaxValueValidator(datetime.today().year),
        ]
    )
    description = models.TextField(
        verbose_name='Описание',
        null=True,
        blank=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='category',
        verbose_name='Категория',
        help_text='Категория, к которой относится произведение'
    )
    genre = models.ManyToManyField(Genre, through='GenreTitle')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('id',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='title',
        verbose_name='Название произведения'
    )
    genre = models.ForeignKey(
        Genre,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='genre',
        verbose_name='Название жанра'
    )

    def __str__(self):
        return f'{self.title}, жанр - {self.genre}'

    class Meta:
        ordering = ('id',)
        verbose_name = 'Жанры произведения'
        verbose_name_plural = 'Жанры произведений'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    text = models.TextField(
        verbose_name='Текст ревью',
        blank=False,
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    score = models.IntegerField(
        verbose_name='Оценка произведения',
        blank=False,
        # Валидаторами ограничиваем диапозон оценки от 1 до 10
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10),
        ]
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        """Устанавливаем сортировку по дате публикации,
        а также требования уникальности связки Автор-Ревью."""
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('pub_date',)
        constraints = [
            models.UniqueConstraint(
                name='unique_review',
                fields=['author', 'title']
            )
        ]

    def __str__(self):
        return f'{self.author}: {self.text[:10]}...'


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        verbose_name='Ревью',
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField(
        verbose_name='Текст комментария',
        blank=False,
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор комментария',
        on_delete=models.CASCADE,
        related_name='comments',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата комментария',
        auto_now_add='True',
        db_index=True
    )

    class Meta:
        """Сортировка по дате создания коммента."""
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('pub_date',)

    def __str__(self):
        return f'{self.author}: {self.text[:10]}...'
