from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Booking
from .serializers import BookingSerializer

# Create your views here.


class BookRoomView(CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer: BookingSerializer):
        serializer.save(guest=self.request.user)

class ListMyBookingsView(ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(guest=self.request.user)

class CancelBookingView(RetrieveDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def perform_destroy(self):
        if self.get_object().guest != self.request.user and not self.request.user.is_superuser:
            raise PermissionError("You can only cancel your own bookings")
        return self.get_object().delete()