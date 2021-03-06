# Generated by Django 3.1.2 on 2020-12-30 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0008_auto_20201228_2152"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="avatar",
            field=models.ImageField(
                default="./avatars/default_avatar.png", upload_to="avatars/"
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="firstname",
            field=models.TextField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name="profile",
            name="lastname",
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]
