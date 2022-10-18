from django.contrib.auth.models import AbstractUser
from django.db import models

CHOICES = (
    ('user', 'USER'),
    ('moderator', 'MODERATOR'),
    ('admin', 'ADMIN')
)


class User(AbstractUser):
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )

    role = models.CharField(
        max_length=20,
        verbose_name='Роль',
        default='user',
        choices=CHOICES,
    )


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField()
    rating = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name="titles",
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        through='TitlesGenres',
        related_name="titles",
        blank=True)

    def __str__(self) -> str:
        return self.name


class TitlesGenres(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} - {self.title}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['genre', 'title'],
                name='unique follow')
        ]


class Review(models.Model):
    text = models.TextField()
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    author = models.ForeignKey(
        User, related_name='reviews',
        on_delete=models.CASCADE,
        blank=True
    )
    score = models.IntegerField()
    pub_date = models.DateTimeField(blank=True)


class Comment(models.Model):
    text = models.TextField()
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    author = models.ForeignKey(
        User, related_name='comments',
        on_delete=models.CASCADE,
        blank=True
    )
    pub_date = models.DateTimeField(blank=True)
