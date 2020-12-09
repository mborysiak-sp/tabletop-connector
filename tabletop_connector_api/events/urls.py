from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import EventViewSet, AddressViewSet, CustomEventAPIView, GameViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet, 'event')
router.register(r'addresses', AddressViewSet, 'address')
router.register(r'games', GameViewSet, 'game')

app_name = 'events'
urlpatterns = [
    path('geteventbydistance/', CustomEventAPIView.as_view())
]

urlpatterns += router.urls
