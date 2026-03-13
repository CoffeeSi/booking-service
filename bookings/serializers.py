from rest_framework import serializers

from typing import Any

from .models import Booking
from users.serializers import UserSerializer
from rooms.serializers import RoomSerializer


class BookingSerializer(serializers.ModelSerializer):
    room = RoomSerializer(read_only=True)
    room_id = serializers.PrimaryKeyRelatedField(
        queryset=RoomSerializer.Meta.model.objects.all(), source="room", write_only=True
    )
    guest = UserSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = [
            "id",
            "room_id",
            "room",
            "guest",
            "start_date",
            "end_date",
        ]

    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        return data
