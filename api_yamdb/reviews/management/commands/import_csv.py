import csv
import os
from django.apps import apps
from django.core.management.base import BaseCommand

from api_yamdb.settings import BASE_DIR
from reviews.models import Title

# Словарь импорта
# [key: имя модели в БД]: {
#   fileName: имя файла CSV,
#   fieldsMatch: словарь соответствия полей из файла, поля в БД
# }

IMPORT_DICTIONARY = {
    "User": {
        "fileName": "users.csv",
        "modelPath": "users.User",
        "fieldsMatch": {
            "id": "id",
            "username": "username",
            "email": "email",
            "role": "role",
            "bio": "bio",
            "first_name": "first_name",
            "last_name": "last_name",
        },
    },
    "Category": {
        "fileName": "category.csv",
        "modelPath": "reviews.Category",
        "fieldsMatch": {
            "id": "id",
            "name": "name",
            "slug": "slug",
        },
    },
    "Genre": {
        "fileName": "genre.csv",
        "modelPath": "reviews.Genre",
        "fieldsMatch": {
            "id": "id",
            "name": "name",
            "slug": "slug",
        },
    },
    "Title": {
        "fileName": "titles.csv",
        "modelPath": "reviews.Title",
        "fieldsMatch": {
            "id": "id",
            "name": "name",
            "year": "year",
            "category": "Category.id",
        },
    },
    "Review": {
        "fileName": "review.csv",
        "modelPath": "reviews.Review",
        "fieldsMatch": {
            "id": "id",
            "title_id": "Title.id",
            "text": "text",
            "author": "User.id",
            "score": "score",
            "pub_date": "pub_date",
        },
    },
    "Comment": {
        "fileName": "comments.csv",
        "modelPath": "reviews.Comment",
        "fieldsMatch": {
            "id": "id",
            "review_id": "Review.id",
            "text": "text",
            "author": "User.id",
            "pub_date": "pub_date",
        },
    },
}


def parse_csv(reader):
    rows = list(reader)
    headers = rows[0]
    result = []
    for r in range(1, len(rows)):
        fields_dict = {}
        for h in range(0, len(headers)):
            fields_dict[headers[h]] = rows[r][h]
        result.insert(r, fields_dict)
    return result


def get_full_record(record_info, fields_match):
    full_record = {}
    for key in fields_match.keys():
        if fields_match[key].find(".id") != -1:
            related_modelName = fields_match[key].split(".")[0]
            related_model = apps.get_model(
                IMPORT_DICTIONARY[related_modelName]["modelPath"]
            )
            print(record_info["id"])
            full_record[key] = related_model.get_or_create(pk=record_info["id"])
        else:
            full_record[key] = record_info.get(key)
    return full_record


def load_data_from_csv_to_model(import_info, reader):
    fields_match = import_info["fieldsMatch"]
    model = apps.get_model(import_info["modelPath"])
    records = parse_csv(reader)

    for record in records:
        full_record = get_full_record(record, fields_match)
        try:
            model.objects.create(**full_record)
        except Exception as e:
            print(f"Ошибка создания записи: {e}")
            exit


class Command(BaseCommand):
    """Заполняет БД."""

    def handle(self, *args, **options):
        for import_info in IMPORT_DICTIONARY.values():
            with open(
                os.path.join(BASE_DIR, "static/data/" + import_info["fileName"]),
                "r",
                encoding="utf-8",
            ) as csv_file:
                reader = csv.reader(csv_file, delimiter=",")
                load_data_from_csv_to_model(import_info, reader)

        #     try:
        #         # ссылка на модель
        #         model_link = MODEL_LINKS[model]
        #         model_link.objects.create(**object_fields)
        #         obj_count += 1
        #     except Exception as e:
        #         print(f'Ошибка создания записи: {e}')
        #         exit

        # for file in files:
