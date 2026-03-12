from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import QuerySet

from .models import Booking
from .serializers import BookingSerializer

# Create your views here.


class BookRoomView(CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer: BookingSerializer) -> None:
        serializer.save(guest=self.request.user)


class ListMyBookingsView(ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet[Booking]:
        return self.queryset.filter(guest=self.request.user)


class CancelBookingView(RetrieveDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance: Booking) -> None:
        if instance.guest != self.request.user and not self.request.user.is_superuser:
            raise PermissionError("You can only cancel your own bookings")
        instance.delete()
