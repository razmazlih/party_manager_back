from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import RegisterView, EventViewSet, ReservationViewSet, CommentViewSet, NotificationViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'reservations', ReservationViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'notifications', NotificationViewSet)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
]

urlpatterns += router.urls