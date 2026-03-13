from rest_framework import serializers

from typing import Any

from .models import Booking
from rooms.serializers import RoomSerializer


class BookingSerializer(serializers.ModelSerializer):
    # room_number = serializers.ReadOnlyField(source="room.room_number")
    room = RoomSerializer(read_only=True)
    room_id = serializers.PrimaryKeyRelatedField(
        queryset=RoomSerializer.Meta.model.objects.all(), source="room", write_only=True
    )
    guest_id = serializers.ReadOnlyField(source="guest.id")
    guest_fullname = serializers.ReadOnlyField(source="guest.__str__")

    class Meta:
        model = Booking
        fields = ["id", "room_id", "room", "guest_id", "guest_fullname", "start_date", "end_date"]

    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        return data
