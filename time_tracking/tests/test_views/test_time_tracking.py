from datetime import timedelta

from django.urls import reverse
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APITestCase

from time_tracking.models import TimeTrackingModel
from time_tracking.serializers import TimeTrackingModelSerializer
from time_tracking.tests.factory import (
    ProjectFactory,
    UserFactory,
    TimeTrackingModelFactory,
)


class AuthenticationTestCase(APITestCase):
    """Class for Authentication test cases."""

    @classmethod
    def setUpTestData(cls) -> None:
        """Set up test data"""
        cls.user = UserFactory(
            username="testuser@test.com",
            password="Test@123",
        )
        cls.user_2 = UserFactory(
            username="testuser2@test.com",
            password="Test@123",
        )
        cls.project = ProjectFactory()
        cls.start_time = timezone.now()
        cls.end_time = timezone.now() + timedelta(hours=1)
        cls.entry_1 = TimeTrackingModelFactory(
            user=cls.user,
            project=cls.project,
            date_worked=timezone.now(),
            hours=3,
        )
        cls.entry_2 = TimeTrackingModelFactory(
            user=cls.user_2,
            project=cls.project,
            date_worked=timezone.now(),
            hours=4,
        )
        cls.entry_3 = TimeTrackingModelFactory(
            user=cls.user,
            project=cls.project,
            date_worked=timezone.now() + timedelta(days=10),
            hours=4,
        )
        cls.time_tracking_url = "time-tracking-list"
        cls.time_tracking_details_url = "time-tracking-detail"

    def test_successful_retrieve_list_of_entries(self):
        """Test successful retrieve list of time tracking entries"""
        self.client.force_authenticate(user=self.user)
        url = reverse(self.time_tracking_url)
        response = self.client.get(url, format="json")

        queryset = TimeTrackingModel.objects.filter(user=self.user)

        serialiazer = TimeTrackingModelSerializer(queryset, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), serialiazer.data)

    def test_successful_retrieve_list_of_entries(self):
        """Test successful retrieve list of time tracking entries"""
        self.client.force_authenticate(user=self.user)
        url = reverse(self.time_tracking_url)
        response = self.client.get(url, format="json")

        queryset = TimeTrackingModel.objects.filter(user=self.user)

        serialiazer = TimeTrackingModelSerializer(queryset, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), serialiazer.data)

    def test_successful_creation_of_an_entry(self):
        """Test successful creation of a time tracking entry"""
        self.client.force_authenticate(user=self.user)
        url = reverse(self.time_tracking_url)

        start_time = timezone.now()
        end_time = start_time + timedelta(hours=2)
        payload = {
            "project": self.project.id,
            "date_worked": timezone.now(),
            "hours": 2,
            "work_description": "Test description",
        }

        response = self.client.post(url, payload, format="json")

        new_entry = TimeTrackingModel.objects.latest("id")

        serialiazer = TimeTrackingModelSerializer(
            new_entry,
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), serialiazer.data)
        self.assertEqual(new_entry.user, self.user)
        self.assertEqual(new_entry.work_description, payload["work_description"])

    def test_successful_retrieval_of_an_entry(self):
        """Test successful retrieval of a time tracking entry"""
        self.client.force_authenticate(user=self.user)
        url = reverse(self.time_tracking_details_url, kwargs={"pk": self.entry_1.id})

        response = self.client.get(url, format="json")

        entry = TimeTrackingModel.objects.get(id=self.entry_1.id)

        serialiazer = TimeTrackingModelSerializer(
            entry,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), serialiazer.data)

    def test_successful_update_of_an_entry(self):
        """Test successful update of a time tracking entry"""
        self.client.force_authenticate(user=self.user)
        payload = {
            "hours": 5,
        }
        url = reverse(self.time_tracking_details_url, kwargs={"pk": self.entry_1.id})

        response = self.client.patch(url, payload, format="json")

        updated_entry = TimeTrackingModel.objects.get(id=self.entry_1.id)

        serialiazer = TimeTrackingModelSerializer(
            updated_entry,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), serialiazer.data)

    def test_successful_delete_of_an_entry(self):
        """Test successful deletion of a time tracking entry"""
        self.client.force_authenticate(user=self.user)

        url = reverse(self.time_tracking_details_url, kwargs={"pk": self.entry_1.id})

        response = self.client.delete(url, format="json")

        entry_exists = TimeTrackingModel.objects.filter(id=self.entry_1.id).exists()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(entry_exists, False)

    def test_unsuccessful_retrieval_of_an_entry(self):
        """Test unsuccessful retrieval of a time tracking entry, not the current user's entry."""
        self.client.force_authenticate(user=self.user)
        url = reverse(self.time_tracking_details_url, kwargs={"pk": self.entry_2.id})

        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.json(), {"detail": "No TimeTrackingModel matches the given query."}
        )

    def test_unsuccessful_retrieval_of_an_entry(self):
        """Test unsuccessful retrieval of a time tracking entry, not the current user's entry."""
        self.client.force_authenticate(user=self.user)
        url = reverse(self.time_tracking_details_url, kwargs={"pk": self.entry_2.id})

        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.json(), {"detail": "No TimeTrackingModel matches the given query."}
        )

    def test_retrieval_of_(self):
        """Test unsuccessful retrieval of a time tracking entry, not the current user's entry."""
        self.client.force_authenticate(user=self.user)
        # Mock a sample query
        start_date = timezone.now().date()
        end_date = timezone.now() + timedelta(days=6)
        url = reverse(self.time_tracking_url, kwargs={})
        response = self.client.get(
            url,
            {"start_date": start_date, "end_date": str(end_date.date())},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
