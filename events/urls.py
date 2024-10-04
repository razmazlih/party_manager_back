from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, EventViewSet, ReservationViewSet, CommentViewSet, NotificationViewSet, get_user_role
from rest_framework.routers import DefaultRouter

# הגדרת ה-Router עבור ה-ViewSets
router = DefaultRouter()
router.register(r'events', EventViewSet, basename='event')
router.register(r'reservations', ReservationViewSet, basename='reservation')
router.register(r'comments', CommentViewSet)
router.register(r'notifications', NotificationViewSet, basename='notification')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/role/', get_user_role, name='get_user_role'),
    path('', include(router.urls)),
]