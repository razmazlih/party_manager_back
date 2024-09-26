from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('organizer', 'Organizer'),
        ('regular', 'Regular User'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    company_name = models.CharField(max_length=100, blank=True, null=True)

class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    date = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.BooleanField(default=True)  # True = Active, False = Inactive
    available_places = models.PositiveIntegerField()
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    reservation_date = models.DateTimeField(auto_now_add=True)
    seats_reserved = models.PositiveIntegerField()

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