# Generated by Django 3.2 on 2023-04-22 08:15

import api_yamdb.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_auto_20230422_0106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.PositiveIntegerField(db_index=True, validators=[api_yamdb.validators.validate_year], verbose_name='Год выпуска'),
        ),
    ]
