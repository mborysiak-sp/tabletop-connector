# Generated by Django 3.1.2 on 2021-01-06 13:43

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chats', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='users',
            field=models.ManyToManyField(blank=True, related_name='chats', to=settings.AUTH_USER_MODEL),
        ),
    ]
