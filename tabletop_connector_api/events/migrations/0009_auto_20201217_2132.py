# Generated by Django 3.1.2 on 2020-12-17 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0008_merge_20201214_1031"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="games",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                related_name="games",
                related_query_name="games",
                to="events.Game",
            ),
        ),
    ]
