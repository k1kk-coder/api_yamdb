import csv

from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from reviews.models import (Category, Comment, Genre, Review, Title,
                            TitlesGenres, User)


class Command(BaseCommand):
    help = 'The Data loader to DB from csv files'

    def load_categories(self):
        url = 'static/data/category.csv'
        with open(url, 'rt', encoding='UTF-8') as f:
            reader = csv.reader(f, dialect="excel")
            next(reader, None)
            for row in reader:
                slug = row[2]
                try:
                    Category.objects.create(id=row[0], name=row[1], slug=slug)
                except IntegrityError as error:
                    print(
                        f'Category. Попытка записи неуникального'
                        f' значения {slug}: {error}')
                except IndexError as error:
                    print(f'Category. Ошибка в структуре файла: {error}')
                except Exception as error:
                    print(f'Category. Неклассифицированная ошибка: {error}')

    def load_genres(self):
        url = 'static/data/genre.csv'
        with open(url, 'rt', encoding='UTF-8') as f:
            reader = csv.reader(f, dialect="excel")
            next(reader, None)
            for row in reader:
                slug = row[2]
                try:
                    Genre.objects.create(id=row[0], name=row[1], slug=slug)
                except IntegrityError as error:
                    print(
                        f'Genre. Попытка записи неуникального значения {slug}:'
                        f' {error}')
                except IndexError as error:
                    print(f'Genre. Ошибка в структуре файла: {error}')
                except Exception as error:
                    print(f'Genre. Неклассифицированная ошибка: {error}')

    def load_title_genres(self):
        url = 'static/data/genre_title.csv'
        with open(url, 'rt', encoding='UTF-8') as f:
            reader = csv.reader(f, dialect="excel")
            next(reader, None)
            for row in reader:
                try:
                    TitlesGenres.objects.create(
                        id=row[0],
                        title=Title.objects.get(id=row[1]),
                        genre=Genre.objects.get(id=row[2]))
                except IntegrityError as error:
                    print(
                        f'TitlesGenres. Попытка записи неуникального значения:'
                        f' {error}')
                except IndexError as error:
                    print(f'TitlesGenres. Ошибка в структуре файла: {error}')
                except Exception as error:
                    print(f'TitlesGenres.'
                          f'Неклассифицированная ошибка: {error}')

    def load_titles(self):
        url = 'static/data/titles.csv'
        with open(url, 'rt', encoding='UTF-8') as f:
            reader = csv.reader(f, dialect="excel")
            next(reader, None)
            for row in reader:
                try:
                    Title.objects.create(
                        id=row[0],
                        name=row[1],
                        year=row[2],
                        category=Category.objects.get(id=row[3]))
                except IndexError as error:
                    print(f'Title. Ошибка в структуре файла: {error}')
                except Exception as error:
                    print(f'Title. Неклассифицированная ошибка: {error}')

    def load_users(self):
        url = 'static/data/users.csv'
        with open(url, 'rt', encoding='UTF-8') as f:
            reader = csv.reader(f, dialect="excel")
            next(reader, None)
            for row in reader:
                try:
                    User.objects.create(
                        id=row[0],
                        username=row[1],
                        email=row[2],
                        role=row[3],
                        bio=row[4],
                        first_name=row[5],
                        last_name=row[6])
                except IndexError as error:
                    print(f'User. Ошибка в структуре файла: {error}')
                except Exception as error:
                    print(f'User. Неклассифицированная ошибка: {error}')

    def load_reviews(self):
        url = 'static/data/review.csv'
        with open(url, 'rt', encoding='UTF-8') as f:
            reader = csv.reader(f, dialect="excel")
            next(reader, None)
            for row in reader:
                try:
                    Review.objects.create(
                        id=row[0],
                        title=Title.objects.get(id=row[1]),
                        text=row[2],
                        author=User.objects.get(id=row[3]),
                        score=row[4],
                        pub_date=row[5])
                except IndexError as error:
                    print(f'Review. Ошибка в структуре файла: {error}')
                except Exception as error:
                    print(f'Review. Неклассифицированная ошибка: {error}')

    def load_comments(self):
        url = 'static/data/comments.csv'
        with open(url, 'rt', encoding='UTF-8') as f:
            reader = csv.reader(f, dialect="excel")
            next(reader, None)
            for row in reader:
                try:
                    Comment.objects.create(
                        id=row[0],
                        review=Review.objects.get(id=row[1]),
                        text=row[2],
                        author=User.objects.get(id=row[3]),
                        pub_date=row[4])
                except IndexError as error:
                    print(f'Review. Ошибка в структуре файла: {error}')
                except Exception as error:
                    print(f'Review. Неклассифицированная ошибка: {error}')

    def handle(self, *args, **kwargs):
        self.load_categories()
        self.load_titles()
        self.load_genres()
        self.load_title_genres()
        self.load_users()
        self.load_reviews()
        self.load_comments()
