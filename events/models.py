from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class User(AbstractUser):
    ROLE_CHOICES = [
        ('organizer', 'Organizer'),
        ('regular', 'Regular User'),
    ]
    is_organizer = models.BooleanField(default=False)

class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    date = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.BooleanField(default=True)
    available_places = models.PositiveIntegerField()
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('cancelled', 'Cancelled'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey('Event', on_delete=models.CASCADE, related_name='reservations')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    reservation_date = models.DateTimeField(auto_now_add=True)  # אם זהו התאריך הרצוי
    seats_reserved = models.PositiveIntegerField(default=1)  # אם זהו מספר המושבים הרצוי
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    verification_code = models.CharField(max_length=100, unique=True, blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.status == 'approved' and not self.verification_code:
            self.verification_code = str(uuid.uuid4())
        super().save(*args, **kwargs)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)