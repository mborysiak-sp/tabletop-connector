# Generated by Django 3.1.2 on 2021-01-02 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0009_auto_20201230_2141"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="avatar",
            field=models.ImageField(
                default="avatars/default_avatar.png", upload_to="avatars/"
            ),
        ),
    ]
