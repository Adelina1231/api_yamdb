# Generated by Django 3.2 on 2023-04-21 22:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_review_title_one_review'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='genretitle',
            options={'ordering': ('id',), 'verbose_name': 'Произведение и жанр', 'verbose_name_plural': 'Произведения и жанры'},
        ),
        migrations.AlterModelOptions(
            name='title',
            options={'ordering': ('-year', 'name'), 'verbose_name': 'Произведение', 'verbose_name_plural': 'Произведения'},
        ),
    ]