from django.contrib import admin
from .models import User, Event, Reservation, Comment, Notification

# רישום מודל המשתמש
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'is_organizer')
    search_fields = ('username', 'email')
    list_filter = ('is_organizer',)

# רישום מודל האירוע
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'date', 'price', 'status', 'available_places', 'organizer')
    search_fields = ('name', 'location')
    list_filter = ('status', 'date', 'organizer')

# רישום מודל ההזמנה
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'reservation_date', 'seats_reserved', 'status')  # עודכן
    search_fields = ('user__username', 'event__name')
    list_filter = ('reservation_date', 'status')  # עודכן

# רישום מודל התגובה
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'content', 'created_at')
    search_fields = ('user__username', 'event__name', 'content')
    list_filter = ('created_at',)

# רישום מודל ההתראה
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'content', 'created_at')
    search_fields = ('user__username', 'title')
    list_filter = ('created_at',)