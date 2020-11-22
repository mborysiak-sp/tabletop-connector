from django.urls import path, include
from django.contrib import admin

from .users import urls as user_urls
from .events import urls as event_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include(user_urls)),
    path('events/', include(event_urls))
]
