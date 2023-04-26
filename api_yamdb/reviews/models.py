from django.contrib.auth.models import AbstractUser
from django.db import models

ADMIN = 'admin'
MODERATOR = 'moderator'
USER = 'user'

ROLES = [
    (ADMIN, ADMIN),
    (MODERATOR, MODERATOR),
    (USER, USER),
]


class User(AbstractUser):
    email = models.EmailField(blank=True, unique=True)
    role = models.CharField(max_length=10, choices=ROLES, default=USER)
    bio = models.TextField(null=True, blank=True)
    password = models.CharField(max_length=128, null=True, blank=True)
    confirmation_code = models.CharField(max_length=200, null=True, blank=True)

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.slug


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.slug


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField(verbose_name='Год релиза')
    description = models.TextField(null=True, verbose_name='Описание')
    genre = models.ManyToManyField(Genre, through='GenreTitle')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        related_name='titles',
        blank=True, null=True)

    def __str__(self) -> str:
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.genre} {self.title}'
