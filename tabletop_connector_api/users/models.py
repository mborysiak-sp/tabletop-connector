import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.username


class Game(models.Model):
    id = models.IntegerField(primary_key=True)
    #users = models.ForeignKey(User, on_delete=)
