from rest_framework import serializers
from .models import User, Event, Reservation, Comment, Notification

class UserSerializer(serializers.ModelSerializer):
    is_organizer = serializers.BooleanField(source='profile.is_organizer', required=False, default=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'is_organizer')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['username'] = validated_data['username'].lower()
        
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            is_organizer=validated_data.get('is_organizer', False)
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class EventSerializer(serializers.ModelSerializer):
    organizer = serializers.ReadOnlyField(source='organizer.username')

    class Meta:
        model = Event
        fields = ['id', 'name', 'description', 'location', 'date', 'price', 'available_places', 'organizer']

class EventNameDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['name', 'date', 'id']

class ReservationSerializer(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField(source='user.username')
    event_name = serializers.ReadOnlyField(source='event.name')  # שם האירוע
    event_date = serializers.ReadOnlyField(source='event.date')  # תאריך האירוע

    class Meta:
        model = Reservation
        fields = ['id', 'event', 'reservation_date', 'event_name', 'user', 'user_name', 'status', 'seats_reserved', 'event_date']        
    def update(self, instance, validated_data):
        if instance.status == 'approved':
            raise serializers.ValidationError("Cannot modify an approved reservation.")
        return super().update(instance, validated_data)

class CommentSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')  # הוספת שם המשתמש לתגובות

    class Meta:
        model = Comment
        fields = ['id', 'event', 'content', 'user', 'username']  # הוספת 'username' לשדות

from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'title', 'content', 'created_at']