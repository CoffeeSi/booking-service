from rest_framework import serializers

from rooms.models import Room


class RoomSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    room_number = serializers.CharField(max_length=10)
    price_per_night = serializers.DecimalField(max_digits=10, decimal_places=2)
    capacity = serializers.IntegerField()

    class Meta:
        model = Room
        fields = ["id", "room_number", "capacity", "price_per_night"]
