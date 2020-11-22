from rest_framework.routers import DefaultRouter

from .views import EventViewSet, AddressViewSet


router = DefaultRouter()
router.register(r'events', EventViewSet, 'event')
router.register(r'addresses', AddressViewSet, 'address')
