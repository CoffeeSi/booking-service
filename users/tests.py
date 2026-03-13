from rest_framework.test import APITestCase
from django.urls import reverse

from .models import User

# Create your tests here.


class UserTests(APITestCase):
    def setUp(self):
        self.user_data = {
            "username": "testuser",
            "email": "testuser@gmail.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "testpassword",
        }

        self.register_url = reverse("register")
        self.login_url = reverse("login")

    def test_registration_success(self):
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 1)

        user = User.objects.get(username="testuser")
        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "User")
        self.assertNotEqual(user.password, "testpassword")
        self.assertTrue(user.check_password("testpassword"))

    def test_registration_duplicate_username_fails(self):
        User.objects.create_user(
            username="testuser",
            first_name="NewTest",
            last_name="NewUser",
            password="testpassword",
        )
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("username", response.data)

    def test_registration_missing_fields_fails(self):
        invalid_data = self.user_data.copy()
        del invalid_data["password"]

        response = self.client.post(self.register_url, invalid_data)
        self.assertEqual(response.status_code, 400)

    def test_login_success(self):
        User.objects.create_user(**self.user_data)
        response = self.client.post(
            self.login_url, {"username": "testuser", "password": "testpassword"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.data)

    def test_login_invalid_credentials_fails(self):
        User.objects.create_user(**self.user_data)
        response = self.client.post(
            self.login_url, {"username": "testuser", "password": "wrongpassword"}
        )
        self.assertEqual(response.status_code, 400)
