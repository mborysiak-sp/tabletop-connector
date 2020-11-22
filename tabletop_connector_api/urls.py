from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib import admin

from .users import views as user_views
from .events import views as event_views


urlpatterns = [
    path('admin/', admin.site.urls),
    include(user_views),
    include(event_views)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
