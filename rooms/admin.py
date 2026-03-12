from django.contrib import admin

from rooms.models import Room

# Register your models here.


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("id", "room_number", "price_per_night", "capacity")
    list_filter = ("capacity",)
    search_fields = ("id", "room_number")
    list_editable = ("room_number", "price_per_night", "capacity")
