from django.urls import path, include
from django.contrib import admin

from .users import urls as user_urls
from .events import urls as event_urls

app_name = 'api'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(user_urls)),
    path('api/', include(event_urls))
]
