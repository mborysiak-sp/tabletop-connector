from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet, ProfileMeAPIView, TokenObtainView
from ..config.common import MEDIA_ROOT

router = DefaultRouter()
router.register(r"profiles", ProfileViewSet)

app_name = "users"
urlpatterns = [
    path("auth/token/login/", TokenObtainView.as_view(), name="token_obtain-view"),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
    path("profiles/me/", ProfileMeAPIView.as_view()),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static('/media/', document_root=MEDIA_ROOT)
urlpatterns += router.urls
