from django.urls import path

from .views import BookRoomView, ListMyBookingsView, CancelBookingView

urlpatterns = [
    path("my/", ListMyBookingsView.as_view(), name="my-bookings"),
    path("book/", BookRoomView.as_view(), name="book-room"),
    path("my/<int:pk>/", CancelBookingView.as_view(), name="cancel-booking"),
]
