from django.conf.urls import url
from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import EventViewSet, AddressViewSet, CustomEventViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet, 'event')
router.register(r'addresses', AddressViewSet, 'address')

app_name = 'events'
urlpatterns = [
    path('geteventbydistance/', CustomEventViewSet.as_view())
]

urlpatterns += router.urls
