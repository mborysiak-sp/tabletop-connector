from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Event


@admin.register(User)
class UserAdmin(UserAdmin):
    pass


admin.site.register(Event)
