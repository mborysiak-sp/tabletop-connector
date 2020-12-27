from django.urls import path, re_path

from rest_framework.routers import DefaultRouter

from .views import EventViewSet, AddressViewSet, CustomEventAPIView, GameViewSet, join_leave_event

router = DefaultRouter()

router.register(r'events', EventViewSet, 'event')
router.register(r'addresses', AddressViewSet, 'address')
router.register(r'games', GameViewSet, 'game')
router.register(r'events', EventViewSet, basename='event')
router.register(r'addresses', AddressViewSet, basename='address')

app_name = 'events'
urlpatterns = [
    path('geteventbydistance/', CustomEventAPIView.as_view()),
    re_path(r'participation/(?P<pk>[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12})/$',
            join_leave_event)
]

urlpatterns += router.urls
