from rest_framework import viewsets, generics
from .models import Event, Reservation, Comment, Notification
from .serializers import EventSerializer, ReservationSerializer, CommentSerializer, NotificationSerializer, UserSerializer
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .models import Event, Reservation, Comment, Notification
from .serializers import EventSerializer, ReservationSerializer, CommentSerializer, NotificationSerializer, UserSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['location', 'date', 'status']  # Filtering by these fields
    search_fields = ['name', 'description']  # Searching in these fields

    def get_queryset(self):
        return Event.objects.filter(status=True)

class ReservationViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['status', 'event__name']

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        reservation = self.get_object()
        if reservation.status == 'approved':
            return Response({'detail': 'Cannot cancel an approved reservation.'}, status=status.HTTP_400_BAD_REQUEST)
        reservation.status = 'cancelled'
        reservation.save()
        return Response({'detail': 'Reservation cancelled successfully.'})

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer