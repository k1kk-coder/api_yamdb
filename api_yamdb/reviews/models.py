from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class User(AbstractUser):
    ADMIN = 'admin'
    USER = 'user'
    MODERATOR = 'moderator'

    CHOICES = (
        (USER, 'user'),
        (ADMIN, 'admin'),
        (MODERATOR, 'moderator')
    )

    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )

    role = models.CharField(
        max_length=50,
        verbose_name='Роль',
        default=USER,
        choices=CHOICES,
    )

    class Meta:
        ordering = ('username',)
        verbose_name = "User"

    @property
    def is_admin(self):
        self.role == User.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        self.role == User.MODERATOR


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Genres'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.PositiveSmallIntegerField(
        verbose_name='Year',
        validators=[MaxValueValidator(2050)],
        db_index=True,
    )
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
        through_fields=('title', 'genre'))

    class Meta:
        verbose_name = 'Titles'

    def __str__(self) -> str:
        return self.name


class TitlesGenres(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['genre', 'title'],
                name='unique follow')
        ]

    def __str__(self):
        return f'{self.genre} - {self.title}'


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
    score = models.PositiveIntegerField(
        verbose_name="rating",
        validators=[
            MinValueValidator(1, 'The score cannot be less than 1'),
            MaxValueValidator(10, 'The score cannot be more than 10')
        ]
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title_review'
            )
        ]
        ordering = ["-pub_date"]
        verbose_name = "Reviews"


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
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = "Comments"
