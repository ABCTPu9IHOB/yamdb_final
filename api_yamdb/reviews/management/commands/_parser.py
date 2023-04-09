import csv

from users.models import User
from reviews.models import Category, Comment, Genre, Review, Title


def users_parser(path):
    with open(path, encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        print('category_parser in progress')
        for row in reader:
            User.objects.create(
                id=row[0],
                username=row[1],
                email=row[2],
                role=row[3],
                bio=row[4],
                first_name=row[5],
                last_name=row[6]
            )
        print('done')


def category_parser(path):
    with open(path, encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        print('category_parser in progress')
        for row in reader:
            Category.objects.create(
                id=row[0],
                name=row[1],
                slug=row[2],
            )
        print('done')


def genre_parser(path):
    with open(path, encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        print('genre_parser in progress')
        for row in reader:
            Genre.objects.create(
                id=row[0],
                name=row[1],
                slug=row[2],
            )
        print('done')


def titles_parser(path):
    with open(path, encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        print('titles_parser in progress')
        for row in reader:
            category = Category.objects.get(id=row[3])
            Title.objects.create(
                id=row[0],
                name=row[1],
                year=row[2],
                category=category,
            )
        print('done')


def genre_title_parser(path):
    with open(path, encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        print('genre_title_parser in progress')
        for row in reader:
            title = Title.objects.get(id=row[1])
            genre = Genre.objects.get(id=row[2])
            title.genre.add(genre)
            title.save()
        print('done')


def review_parser(path):
    with open(path, encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        print('review_parser in progress')
        for row in reader:
            title = Title.objects.get(id=row[1])
            author = User.objects.get(id=row[3])
            Review.objects.create(
                id=row[0],
                title=title,
                text=row[2],
                author=author,
                score=row[4],
                pub_date=row[5],
            )
        print('done')


def comments_parser(path):
    with open(path, encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        print('comment_parser in progress')
        for row in reader:
            review = Review.objects.get(id=row[0])
            author = User.objects.get(id=row[3])
            Comment.objects.create(
                id=row[0],
                review=review,
                text=row[2],
                author=author,
                pub_date=row[4],
            )
        print('done')
