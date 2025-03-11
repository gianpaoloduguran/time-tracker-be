from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from time_tracking.models import ProjectsModel
from time_tracking.serializers import ProjectsSerializer
from time_tracking.tests.factory import ProjectFactory, UserFactory


class AuthenticationTestCase(APITestCase):
    """Class for Authentication test cases."""

    @classmethod
    def setUpTestData(cls) -> None:
        """Set up test data"""
        cls.user = UserFactory(
            username="testuser@test.com",
            password="Test@123",
        )
        cls.project = ProjectFactory()

        cls.project_url = "project-list"
        cls.project_details_url = "project-detail"

    def test_successful_retrieve_project_list(self):
        """Test successful retrieve of project list."""
        self.client.force_authenticate(user=self.user)
        url = reverse(self.project_url)

        response = self.client.get(url, format="json")
        # Simulate the response data
        queryset = ProjectsModel.objects.filter(is_deleted=False)

        serialiazer = ProjectsSerializer(queryset, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), serialiazer.data)

    def test_successful_creation_of_a_project(self):
        """Test successful creation of a project."""
        self.client.force_authenticate(user=self.user)
        url = reverse(self.project_url)

        payload = {"title": "Test Title"}

        response = self.client.post(url, payload, format="json")
        # Simulate the response data
        new_project = ProjectsModel.objects.latest("id")

        serialiazer = ProjectsSerializer(new_project)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), serialiazer.data)
        self.assertEqual(response.json()["id"], new_project.id)
        self.assertEqual(response.json()["title"], new_project.title)

    def test_successful_creation_of_a_project(self):
        """Test successful creation of a project."""
        self.client.force_authenticate(user=self.user)
        url = reverse(self.project_url)

        payload = {"title": "Test Title"}

        response = self.client.post(url, payload, format="json")
        # Simulate the response data
        new_project = ProjectsModel.objects.latest("id")

        serialiazer = ProjectsSerializer(new_project)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), serialiazer.data)
        self.assertEqual(response.json()["id"], new_project.id)
        self.assertEqual(response.json()["title"], payload["title"])

    def test_successful_retrieval_of_a_project(self):
        """Test successful retireval of a project."""
        self.client.force_authenticate(user=self.user)
        url = reverse(self.project_details_url, kwargs={"pk": self.project.id})

        response = self.client.get(url, format="json")
        # Simulate the response data
        project = ProjectsModel.objects.get(id=self.project.id)

        serialiazer = ProjectsSerializer(project)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), serialiazer.data)

    def test_successful_update_of_a_project(self):
        """Test successful update of a project."""
        self.client.force_authenticate(user=self.user)
        url = reverse(self.project_details_url, kwargs={"pk": self.project.id})

        payload = {"title": "Test Title Update"}

        response = self.client.patch(url, payload, format="json")
        # Simulate the response data
        updated_project = ProjectsModel.objects.get(id=self.project.id)

        serialiazer = ProjectsSerializer(updated_project)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), serialiazer.data)
        self.assertEqual(response.json()["title"], payload["title"])

    def test_successful_soft_delete_of_a_project(self):
        """Test successful soft deletion of a project."""
        self.client.force_authenticate(user=self.user)
        url = reverse(self.project_details_url, kwargs={"pk": self.project.id})

        response = self.client.delete(url, format="json")

        updated_project = ProjectsModel.objects.get(id=self.project.id)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(updated_project.is_deleted, True)

    def test_unsuccessful_retireval_of_a_project(self):
        """Test unsuccessful retrieval of a project given wrong id."""
        self.client.force_authenticate(user=self.user)
        url = reverse(self.project_details_url, kwargs={"pk": 500})

        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.json(), {"detail": "No ProjectsModel matches the given query."}
        )

    def test_unsuccessful_retireval_of_a_project(self):
        """Test unsuccessful creation of a project title is taken."""
        self.client.force_authenticate(user=self.user)
        url = reverse(self.project_url)

        payload = {"title": self.project.title}
        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(), {"title": ["Project title is already taken."]}
        )

    def test_unsuccessful_acceess(self):
        """Test unsuccessful retrieval of a project given wrong id."""
        url = reverse(self.project_url)

        payload = {"title": "Test title access"}
        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.json(),
            {"detail": "Authentication credentials were not provided."},
        )
