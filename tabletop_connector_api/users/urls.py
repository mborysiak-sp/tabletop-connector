from rest_framework.routers import DefaultRouter

from django.urls import path, include

from .views import ProfileViewSet, return_me

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet)

app_name = 'users'
urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/', include('djoser.urls.authtoken')),
    path('profiles/me/', return_me)
]

urlpatterns += router.urls
