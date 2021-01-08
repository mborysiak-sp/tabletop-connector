from django.urls import path, re_path
from rest_framework.routers import DefaultRouter

from .views import ChatModelViewSet

router = DefaultRouter()

router.register(r"chats", ChatModelViewSet, basename="address")

app_name = "chats"
urlpatterns = [
]

urlpatterns += router.urls
