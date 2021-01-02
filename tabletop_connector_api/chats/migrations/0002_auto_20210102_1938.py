# Generated by Django 3.1.2 on 2021-01-02 19:38

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chats', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default='2010-10-10'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='chat',
            name='users',
            field=models.ManyToManyField(blank=True, null=True, related_name='chats', to=settings.AUTH_USER_MODEL),
        ),
    ]
