from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from time_tracking.tests.factory import UserFactory

# Create your tests here.


class AuthenticationTestCase(APITestCase):
    """Class for Authentication test cases."""

    def setUp(self):
        self.client = APIClient()
        self.maxDiff = None  # pylint: disable=C0103

    @classmethod
    def setUpTestData(cls) -> None:
        """Set up test data"""
        cls.user = UserFactory(
            username="testuser@test.com",
            password="Test@123",
        )

        cls.login_url = "login"
        cls.register_url = "register-list"

    def test_successful_login(self):
        """Test successful login for a user."""
        url = reverse(self.login_url)

        payload = {"username": self.user.username, "password": "Test@123"}
        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if refresh and access token in the response
        self.assertIn("refresh", response.data)
        self.assertIn("access", response.data)

    def test_unsuccessful_login(self):
        """Test unsuccessful login for a user if invalid credentials are given"""
        url = reverse(self.login_url)

        payload = {"username": self.user.username, "password": "Test@123123"}
        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.json(),
            {"detail": "No active account found with the given credentials"},
        )

    def test_successful_register_user(self):
        """Test successful register for a user"""
        url = reverse(self.register_url)

        payload = {"username": "testuser2@test.com", "password": "Test@123"}
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Check if refresh and access token in the response
        self.assertIn("refresh", response.data)
        self.assertIn("access", response.data)

        # Check if the user can login
        url = reverse(self.login_url)
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if refresh and access token in the response
        self.assertIn("refresh", response.data)
        self.assertIn("access", response.data)

    def test_successful_register_user_no_password_given(self):
        """Test unsucessful register no password is given"""
        url = reverse(self.register_url)

        payload = {
            "username": "testuser3@test.com",
        }
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {"password": ["This field is required."]})

    def test_successful_register_user_no_username_given(self):
        """Test unsucessful register no username is given"""
        url = reverse(self.register_url)

        payload = {
            "password": "Test@123",
        }
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {"username": ["This field is required."]})

    def test_successful_register_user_username_taken(self):
        """Test unsucessful register username is taken."""
        url = reverse(self.register_url)

        payload = {
            "username": self.user.username,
            "password": "Test@123",
        }
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {"username": ["This email/username has already been taken."]},
        )
