from rest_framework import viewsets, generics
from .models import Event, Reservation, Comment, Notification
from .serializers import EventSerializer, ReservationSerializer, CommentSerializer, NotificationSerializer, UserSerializer
from rest_framework import viewsets, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from rest_framework.exceptions import NotAuthenticated
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .models import Event, Reservation, Comment, Notification
from .serializers import EventSerializer, ReservationSerializer, CommentSerializer, NotificationSerializer, UserSerializer, EventNameDateSerializer
from events import serializers

class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def organizer(self, request):
        user = request.user
        if not user.is_organizer:
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

class EventNameDateListView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        events = Event.objects.all()
        serializer = EventNameDateSerializer(events, many=True)
        return Response(serializer.data)

class ReservationViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['status', 'event__name']

    def get_queryset(self):
        if self.request.user.is_anonymous:
            raise NotAuthenticated("User must be authenticated to view reservations.")
        
        # אם המשתמש הוא מארגן, אפשר לו לראות את כל ההזמנות לאירועים שהוא יצר
        if self.request.user.is_organizer:
            return Reservation.objects.filter(event__organizer=self.request.user).order_by('-created_at')
        
        # אחרת, המשתמש רואה רק את ההזמנות שלו
        return Reservation.objects.filter(user=self.request.user).order_by('-created_at')

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
        reservation = serializer.save(user=self.request.user)

        # יצירת התראה עבור המשתמש
        Notification.objects.create(
            user=self.request.user,
            title="Reservation Pending Approval",
            content=f"Your ticket reservation for the event {event.name} is awaiting the organizer's approval."
        )

        return Response({'id': reservation.id, 'message': 'Reservation created successfully'}, status=status.HTTP_201_CREATED)

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

        Notification.objects.create(
            user=self.request.user,
            title="Reservation Canceled",
            content=f"Your ticket reservation for the event {event.name} is canceled."
        )

        return Response({'detail': 'Reservation cancelled successfully.'})
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def approve(self, request, pk=None):
        reservation = self.get_object()

        if reservation.event.organizer != request.user:
            return Response({'detail': 'Not authorized.'}, status=status.HTTP_403_FORBIDDEN)
        
        reservation.status = 'approved'
        reservation.save()

        Notification.objects.create(
            user=reservation.user,
            title="Reservation Approved",
            content=f"Your ticket reservation for the event {reservation.event.name} is approved. See you there!"
        )

        return Response({'status': 'Reservation approved'})

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def reject(self, request, pk=None):
        reservation = self.get_object()
        
        # בדוק אם המשתמש המחובר הוא המארגן של האירוע
        if reservation.event.organizer != request.user:
            return Response({'detail': 'Not authorized. Only the organizer can reject reservations.'}, status=status.HTTP_403_FORBIDDEN)
        
        # דחיית ההזמנה
        reservation.status = 'rejected'
        reservation.save()
        
        event = reservation.event
        event.available_places += reservation.seats_reserved
        event.save()

        Notification.objects.create(
            user=reservation.user,
            title="Reservation Rejected",
            content=f"Your ticket reservation for the event {event.name} has been rejected."
        )

        return Response({'status': 'Reservation rejected and available places updated'})
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def verify_event_code(self, request, pk=None):
        event_id = pk
        verification_code = request.data.get('verification_code')
        
        reservations = Reservation.objects.filter(event_id=event_id)

        for reservation in reservations:
            if reservation.verification_code == verification_code:
                if reservation.is_verified:
                    return Response({
                        'status': 'Already scanned',
                        'user_name': reservation.user.username
                    }, status=status.HTTP_200_OK)
                else:
                    reservation.is_verified = True
                    reservation.save()
                    return Response({
                        'status': 'Verification successful',
                        'user_name': reservation.user.username
                    }, status=status.HTTP_200_OK)
        
        return Response({'status': 'Invalid verification code'}, status=status.HTTP_400_BAD_REQUEST)

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
def user_is_organizer(request):
    user = request.user
    return Response({'is_organizer': user.is_organizer})