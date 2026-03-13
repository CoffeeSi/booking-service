from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django.db.models import QuerySet
from django.db import transaction

from rooms import serializers
from rooms.models import Room

from .models import Booking
from .serializers import BookingSerializer
from .permissions import IsBookingOwnerOrSuperuser

# Create your views here.


class BookRoomView(CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer: BookingSerializer) -> None:
        try:
            # Use a transaction to block the room in database until the booking is created
            with transaction.atomic():
                room = serializer.validated_data["room"]
                Room.objects.select_for_update().get(id=room.id)

                serializer.save(guest=self.request.user)

        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)


class ListMyBookingsView(ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet[Booking]:
        return self.queryset.filter(guest=self.request.user)


class RetrieveCancelBookingView(RetrieveDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated, IsBookingOwnerOrSuperuser]
