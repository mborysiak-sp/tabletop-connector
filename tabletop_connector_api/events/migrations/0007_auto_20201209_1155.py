# Generated by Django 3.1.2 on 2020-12-09 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_auto_20201209_0924'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='thumbnail',
            field=models.CharField(default='asdasdasda', max_length=512),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='game',
            name='name',
            field=models.CharField(max_length=512),
        ),
    ]