from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from .users import urls as user_urls

urlpatterns = [
    path('api/v1/', include(user_urls))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
