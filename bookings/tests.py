from django.utils import timezone
from datetime import timedelta
from django.urls import reverse
from rest_framework.test import APITestCase

from .models import Booking
from users.models import User
from rooms.models import Room

# Create your tests here.


class BookingTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            first_name="Test",
            last_name="User",
            email="testuser@gmail.com",
            password="password123",
        )
        self.room = Room.objects.create(
            room_number="101", price_per_night=2000, capacity=2
        )

        self.create_url = reverse("book-room")
        self.list_url = reverse("my-bookings")

    def test_create_booking_success(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "room_id": self.room.id,
            "start_date": timezone.now().date() + timedelta(days=1),
            "end_date": timezone.now().date() + timedelta(days=3),
        }
        response = self.client.post(self.create_url, data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Booking.objects.count(), 1)
        self.assertEqual(Booking.objects.first().guest, self.user)

    def test_overlap_booking_fails(self):
        self.client.force_authenticate(user=self.user)

        start_existing = timezone.now().date() + timedelta(days=10)
        end_existing = timezone.now().date() + timedelta(days=15)
        Booking.objects.create(
            room=self.room,
            guest=self.user,
            start_date=start_existing,
            end_date=end_existing,
        )

        data = {
            "room_id": self.room.id,
            "start_date": timezone.now().date() + timedelta(days=14),
            "end_date": timezone.now().date() + timedelta(days=18),
        }
        response = self.client.post(self.create_url, data)

        self.assertEqual(response.status_code, 400)
        self.assertIn("not available", str(response.data))

    def test_start_date_in_past_fails(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "room_id": self.room.id,
            "start_date": timezone.now().date() - timedelta(days=1),
            "end_date": timezone.now().date() + timedelta(days=2),
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, 400)

    def test_get_my_bookings(self):
        Booking.objects.create(
            room=self.room,
            guest=self.user,
            start_date=timezone.now().date() + timedelta(days=1),
            end_date=timezone.now().date() + timedelta(days=2),
        )

        other_user = User.objects.create_user(username="other", password="pass")
        Booking.objects.create(
            room=self.room,
            guest=other_user,
            start_date=timezone.now().date() + timedelta(days=5),
            end_date=timezone.now().date() + timedelta(days=6),
        )

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url)

        results = response.data.get("results", response.data)
        self.assertEqual(len(results), 1)
