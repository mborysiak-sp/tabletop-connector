from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ProfileViewSet, ProfileMeAPIView, TokenObtainView

router = DefaultRouter()
router.register(r"profiles", ProfileViewSet)

app_name = "users"
urlpatterns = [
    path("auth/token/login/", TokenObtainView.as_view(), name="token_obtain-view"),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
    path("profiles/me/", ProfileMeAPIView.as_view()),
]

urlpatterns += router.urls
