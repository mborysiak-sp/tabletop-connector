# Generated by Django 3.1.2 on 2020-12-09 09:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0005_auto_20201206_1231"),
    ]

    operations = [
        migrations.AlterField(
            model_name="game",
            name="max_players",
            field=models.PositiveIntegerField(
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(100),
                ]
            ),
        ),
        migrations.AlterField(
            model_name="game",
            name="min_players",
            field=models.PositiveIntegerField(
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(100),
                ]
            ),
        ),
        migrations.AlterField(
            model_name="game",
            name="playtime",
            field=models.PositiveIntegerField(
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(1000),
                ]
            ),
        ),
    ]
