from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError as DRFValidationError
from django.core.exceptions import ValidationError
from django.db.models import QuerySet
from django.db import transaction
from drf_spectacular.utils import extend_schema, OpenApiExample

from rooms.models import Room
from .models import Booking
from .serializers import BookingSerializer
from .permissions import IsBookingOwnerOrSuperuser

# Create your views here.


@extend_schema(
    summary="Book a Room",
    description="Create a new booking for a specific room and selected dates",
    request=BookingSerializer,
    responses=BookingSerializer,
    examples=[
        OpenApiExample(
            "Booking Creation",
            value={
                "id": 1,
                "room_id": 1,
                "start_date": "2026-03-14",
                "end_date": "2026-03-21",
            },
        )
    ],
)
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
            raise DRFValidationError(e.message_dict)


@extend_schema(
    summary="List My Bookings",
    description="Get a list of all bookings made by an user",
    responses=BookingSerializer(many=True),
    examples=[
        OpenApiExample(
            "Successful Retrieval of User Bookings",
            value={
                "count": 2,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": 1,
                        "room": {
                            "id": 1,
                            "room_number": "101",
                            "price_per_night": 200.00,
                            "capacity": 2,
                        },
                        "guest": {
                            "id": 1,
                            "username": "testuser",
                            "first_name": "Test",
                            "last_name": "User",
                            "email": "testuser@gmail.com",
                        },
                        "start_date": "2026-03-13",
                        "end_date": "2026-03-21",
                    }
                ],
            },
        )
    ],
)
class ListMyBookingsView(ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet[Booking]:
        return self.queryset.filter(guest=self.request.user)


@extend_schema(
    summary="Retrieve or Cancel a Booking",
    description="Retrieve details of a specific booking or cancel it by deleting the booking.",
    responses=BookingSerializer,
    examples=[
        OpenApiExample(
            "Successful Retrieval of Booking Details",
            value={
                "id": 1,
                "room": {
                    "id": 1,
                    "room_number": "101",
                    "price_per_night": 200.00,
                    "capacity": 2,
                },
                "guest": {
                    "id": 1,
                    "username": "testuser",
                    "first_name": "Test",
                    "last_name": "User",
                    "email": "testuser@gmail.com",
                },
                "start_date": "2026-03-13",
                "end_date": "2026-03-21",
            },
        )
    ],
)
class RetrieveCancelBookingView(RetrieveDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated, IsBookingOwnerOrSuperuser]
