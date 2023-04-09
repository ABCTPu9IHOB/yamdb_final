import os

from api_yamdb.settings import BASE_DIR
from django.core.management.base import BaseCommand

from ._parser import category_parser
from ._parser import comments_parser
from ._parser import genre_parser
from ._parser import genre_title_parser
from ._parser import review_parser
from ._parser import titles_parser
from ._parser import users_parser


class Command(BaseCommand):

    def handle(self, *args, **options):

        parser_dict = {
            'users': users_parser,
            'category': category_parser,
            'genre': genre_parser,
            'titles': titles_parser,
            'genre_title': genre_title_parser,
            'review': review_parser,
            'comments': comments_parser,
        }

        for name_csv, parser in parser_dict.items():
            path = os.path.join(BASE_DIR, f'static/data/{name_csv}.csv')
            parser_object = parser_dict[name_csv]
            parser_object(path)
