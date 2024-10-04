from rest_framework import viewsets, generics
from .models import Event, Reservation, Comment, Notification
from .serializers import EventSerializer, ReservationSerializer, CommentSerializer, NotificationSerializer, UserSerializer
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from rest_framework.exceptions import NotAuthenticated
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .models import Event, Reservation, Comment, Notification
from .serializers import EventSerializer, ReservationSerializer, CommentSerializer, NotificationSerializer, UserSerializer
from events import serializers

class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def organizer(self, request):
        user = request.user
        if user.role != 'organizer':
            return Response({'detail': 'Not authorized.'}, status=status.HTTP_403_FORBIDDEN)
        events = Event.objects.filter(organizer=user)
        serializer = self.get_serializer(events, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def pending_reservations(self, request, pk=None):
        event = self.get_object()
        if event.organizer != request.user:
            return Response({'detail': 'Not authorized.'}, status=status.HTTP_403_FORBIDDEN)
        reservations = Reservation.objects.filter(event=event, status='pending')
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        return Event.objects.filter(status=True)

class ReservationViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['status', 'event__name']

    def get_queryset(self):
        # בדיקה אם המשתמש מחובר
        if self.request.user.is_anonymous:
            raise NotAuthenticated("User must be authenticated to view reservations.")

        # מחזיר את ההזמנות של המשתמש המחובר
        return Reservation.objects.filter(user=self.request.user).order_by('-created_at')  # מיון מההזמנות החדשות לישנות

    def perform_create(self, serializer):
        event = serializer.validated_data['event']
        seats_reserved = serializer.validated_data.get('seats_reserved', 1)

        # בדיקה אם יש מספיק מקומות פנויים
        if event.available_places < seats_reserved:
            raise serializers.ValidationError("Not enough available places for this reservation.")

        # הפחתת מספר המושבים הפנויים באירוע
        event.available_places -= seats_reserved
        event.save()

        # שמירת ההזמנה
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        reservation = self.get_object()
        if reservation.status == 'approved':
            return Response({'detail': 'Cannot cancel an approved reservation.'}, status=status.HTTP_400_BAD_REQUEST)

        # החזרת מספר המקומות הפנויים באירוע במקרה של ביטול
        event = reservation.event
        event.available_places += reservation.seats_reserved
        event.save()

        # עדכון הסטטוס של ההזמנה ל-"cancelled"
        reservation.status = 'cancelled'
        reservation.save()
        return Response({'detail': 'Reservation cancelled successfully.'})
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def approve(self, request, pk=None):
        reservation = self.get_object()
        if reservation.event.organizer != request.user:
            return Response({'detail': 'Not authorized.'}, status=status.HTTP_403_FORBIDDEN)
        reservation.status = 'approved'
        reservation.save()
        return Response({'status': 'Reservation approved'})
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def reject(self, request, pk=None):
        reservation = self.get_object()
        if reservation.event.organizer != request.user:
            return Response({'detail': 'Not authorized.'}, status=status.HTTP_403_FORBIDDEN)
        reservation.status = 'rejected'
        reservation.save()
        return Response({'status': 'Reservation rejected'})

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['event']

    def perform_create(self, serializer):
        user = self.request.user
        event = serializer.validated_data['event']
        
        # בדיקה אם למשתמש יש כבר תגובה עבור האירוע הזה
        if Comment.objects.filter(event=event, user=user).exists():
            raise serializers.ValidationError("You have already added a comment for this event.")
        
        # יצירת תגובה חדשה אם אין תגובה קיימת
        serializer.save(user=user)

class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]  # ודא שרק משתמשים מחוברים יכולים לראות את ההודעות

    def get_queryset(self):
        # מחזיר רק את ההודעות של המשתמש המחובר
        user = self.request.user
        return Notification.objects.filter(user=user)
    
@api_view(['GET'])
def get_user_role(request):
    user = request.user
    return Response({'role': user.role})