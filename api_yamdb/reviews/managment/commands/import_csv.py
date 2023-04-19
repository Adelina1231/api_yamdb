import csv
import os
from django.core.management.base import BaseCommand

from api_yamdb.settings import BASE_DIR
from reviews.models import Title

class Command(BaseCommand):
    """Заполняет БД."""

    def handle(self, *args, **options):
        files = (
            "category.csv",
            "comments.csv",
            "genre_title.csv",
            "genre.csv",
            "review.csv",
            "titles.csv",
            "users.csv"
        )
        for file in files:
            with open(os.path.join(
                BASE_DIR, 'static/data/' + file), "r"
            ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=",")
                model_list = []
                for row in csv_reader:
                    if file == 'titles.csv':
                        model_list.append(Title(
                            name=row["name"], id=row["id"], slug=row["slug"]))
                        model_list.save()
