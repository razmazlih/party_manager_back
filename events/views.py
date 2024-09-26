from rest_framework import viewsets, generics
from .models import Event, Reservation, Comment, Notification
from .serializers import EventSerializer, ReservationSerializer, CommentSerializer, NotificationSerializer, UserSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_queryset(self):
        return Event.objects.filter(status=True)

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer