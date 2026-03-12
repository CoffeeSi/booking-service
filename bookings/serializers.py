from django.utils import timezone
from django.db import transaction
from rest_framework import serializers

from typing import Any

from rooms.models import Room
from .models import Booking


class BookingSerializer(serializers.ModelSerializer):
    guest_id = serializers.ReadOnlyField(source="guest.id")

    class Meta:
        model = Booking
        fields = ["id", "room", "guest_id", "start_date", "end_date"]

    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        # Use a transaction to block the room in database until the booking is created
        with transaction.atomic():
            room = data["room"]

            Room.objects.select_for_update().get(id=room.id)

            start_date = data["start_date"]
            end_date = data["end_date"]

            if not self.room or not self.guest:
                raise serializers.ValidationError("Room and guest must be specified")
            if self.start_date is None or self.end_date is None:
                raise serializers.ValidationError(
                    "Start date and end date must be specified"
                )
            if start_date >= end_date:
                raise serializers.ValidationError("End date must be after start date")
            if start_date < timezone.now().date():
                raise serializers.ValidationError("Start date cannot be in the past")
            if Booking.objects.filter(
                room=room, start_date__lt=end_date, end_date__gt=start_date
            ).exists():
                raise serializers.ValidationError(
                    "This room is not available for the selected dates"
                )
            return data
