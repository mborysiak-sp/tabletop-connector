from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


app_name = 'users'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
