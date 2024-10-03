from rest_framework import serializers
from .models import User, Event, Reservation, Comment, Notification

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'role', 'company_name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            role=validated_data.get('role', 'regular'),
            company_name=validated_data.get('company_name', '')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class ReservationSerializer(serializers.ModelSerializer):
    event_name = serializers.ReadOnlyField(source='event.name')  # שם האירוע
    event_date = serializers.ReadOnlyField(source='event.date')  # תאריך האירוע

    class Meta:
        model = Reservation
        fields = '__all__'  # מחזיר את כל השדות הקיימים

    def update(self, instance, validated_data):
        if instance.status == 'approved':
            raise serializers.ValidationError("Cannot modify an approved reservation.")
        return super().update(instance, validated_data)

class CommentSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')  # הוספת שם המשתמש לתגובות

    class Meta:
        model = Comment
        fields = ['id', 'event', 'content', 'user', 'username']  # הוספת 'username' לשדות

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'