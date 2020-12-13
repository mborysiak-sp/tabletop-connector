# Generated by Django 3.1.2 on 2020-12-06 11:31

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_auto_20201124_0931'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128)),
                ('image', models.CharField(max_length=512)),
                ('min_players', models.IntegerField()),
                ('max_players', models.IntegerField()),
                ('playtime', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='games',
            field=models.ManyToManyField(related_name='games', related_query_name='games', to='events.Game'),
        ),
    ]