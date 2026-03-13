from rest_framework.test import APITestCase
from django.urls import reverse

from .models import Room

# Create your tests here.


class RoomTests(APITestCase):
    def setUp(self):
        self.room_101 = Room.objects.create(
            room_number="101", capacity=1, price_per_night=1900.00
        )
        self.room_201 = Room.objects.create(
            room_number="201", capacity=2, price_per_night=150.00
        )

        self.url = reverse("list-rooms")

    def test_list_rooms(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data.get("results", [])), 2)

    def test_filter_rooms_by_capacity(self):
        response = self.client.get(self.url, {"capacity": 2})
        results = response.data.get("results", [])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(results), 1)
        self.assertEqual(response.data.get("results", [])[0]["room_number"], "201")

    def test_filter_rooms_by_price_range(self):
        response = self.client.get(self.url, {"min_price": 1000, "max_price": 2000})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data.get("results", [])), 1)
        self.assertEqual(response.data.get("results", [])[0]["room_number"], "101")

    def test_sorting_by_price(self):
        response = self.client.get(self.url, {"ordering": "price_per_night"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("results", [])[0]["room_number"], "201")
