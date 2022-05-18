import csv
import os
from django.core.management.base import BaseCommand
from reviews.models import Review
import sqlite3
# from django.db import connection
from django.conf import settings


class Command(BaseCommand):
    help = 'The Zen of Python'

    def handle(self, *args, **options):
        list_files = {
            'users': 'reviews_user',
            'category': 'reviews_categorie', 'genre': 'reviews_genre',
            'titles': 'reviews_title', 'genre_title': 'reviews_title_genre',
            'review': 'reviews', 'comments': 'reviews_comment'
        }
        dir_files = os.path.join(settings.STATICFILES_DIRS[0], "data")
        print(dir_files)
        # for file_name in list_files:
        file_name = list(list_files.keys())[6] + '.csv'
        file_name = os.path.join(dir_files, file_name)
        one_file = open(file_name)
        reader = csv.reader(one_file)
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        for row in reader:
            if row[0].isnumeric():
                row[2] = row[2].replace("'", ".")
                title_id = Review.objects.get(id=row[1]).title.id
                query = f"INSERT into {list_files['comments']} values ({row[0]}, '{row[2]}', '{row[4]}', {row[3]}, {row[1]}, {title_id})"
                cursor.execute(query)
            else:
                print(row)
        conn.commit()
        conn.close()
        one_file.close()
