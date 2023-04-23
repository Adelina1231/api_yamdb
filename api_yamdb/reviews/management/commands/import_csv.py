import csv
import os
from django.apps import apps
from django.core.management.base import BaseCommand
from api_yamdb.settings import BASE_DIR


class Bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


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
    "GenreTitle": {
        "fileName": "genre_title.csv",
        "modelPath": "reviews.GenreTitle",
        "fieldsMatch": {
            "id": "id",
            "title_id": "Title.id",
            "genre_id": "Genre.id",
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

    for row in rows[1:]:
        fields_dict = {}
        for i, header in enumerate(headers):
            fields_dict[header] = row[i]
        result.append(fields_dict)

    return result


def get_full_record(record_info, fields_match):
    full_record = {}
    for key in fields_match.keys():
        if fields_match[key].find(".id") != -1:
            related_modelName = fields_match[key].split(".")[0]
            related_model = apps.get_model(
                IMPORT_DICTIONARY[related_modelName]["modelPath"]
            )
            related_object = related_model.objects.get(id=record_info[key])
            if key.find("_id") != -1:
                full_record[key] = related_object.id
            else:
                full_record[key] = related_object

        else:
            full_record[key] = record_info.get(key)
    return full_record


def load_data_from_csv_to_model(import_info, reader):
    fields_match = import_info["fieldsMatch"]
    model = apps.get_model(import_info["modelPath"])
    print(
        (
            f"\n→ {Bcolors.OKCYAN}Загрузка CSV для таблицы: "
            f'{import_info["modelPath"]}...{Bcolors.ENDC}'
        )
    )
    records = parse_csv(reader)
    print(f"→ {Bcolors.BOLD}Обнаружено записей: {len(records)}.{Bcolors.ENDC}")
    for record in records:
        full_record = get_full_record(record, fields_match)
        try:
            model.objects.update_or_create(**full_record)
        except Exception as e:
            print(f"{Bcolors.FAIL}Ошибка создания записи: {e}{Bcolors.ENDC}")
            exit
    print(
        (
            f'→ {Bcolors.OKGREEN}Таблица {import_info["modelPath"]} '
            f"успешно обновлена!{Bcolors.ENDC}"
        )
    )


class Command(BaseCommand):
    """Заполняет БД."""

    def handle(self, *args, **options):
        for im_inf in IMPORT_DICTIONARY.values():
            with open(
                os.path.join(BASE_DIR, f'static/data/{im_inf["fileName"]}'),
                "r",
                encoding="utf-8",
            ) as csv_file:
                reader = csv.reader(csv_file, delimiter=",")
                load_data_from_csv_to_model(im_inf, reader)
