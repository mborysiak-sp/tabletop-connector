from rest_framework.routers import DefaultRouter

from django.urls import path, include

from .views import UserViewSet, ProfileViewSet


router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'profiles', ProfileViewSet)

app_name = 'users'
urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/', include('djoser.urls.authtoken')),
]

urlpatterns += router.urls
