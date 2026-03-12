from django.contrib import admin

from bookings.models import Booking

# Register your models here.


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "room", "guest", "start_date", "end_date")
    list_filter = ("start_date", "end_date", "room")
    search_fields = ("guest__username", "room__room_number")
    list_editable = ("room", "guest", "start_date", "end_date")
