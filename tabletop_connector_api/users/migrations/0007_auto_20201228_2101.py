# Generated by Django 3.1.2 on 2020-12-28 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0006_auto_20201220_1424"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="firstname",
            field=models.TextField(default="dupa", max_length=64),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="profile",
            name="lastname",
            field=models.CharField(default="dupa", max_length=64),
            preserve_default=False,
        ),
    ]
