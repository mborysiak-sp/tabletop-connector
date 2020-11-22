from rest_framework.routers import DefaultRouter

from django.contrib import admin
from django.urls import path, include

from .views import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)

app_name = 'users'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('api/auth/', include('djoser.urls.authtoken')),
]

urlpatterns += router.urls
