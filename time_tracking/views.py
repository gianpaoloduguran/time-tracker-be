from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet


from time_tracking.filters import TimeTrackingModelFilter
from time_tracking.models import ProjectsModel, TimeTrackingModel
from time_tracking.serializers import (
    ProjectsSerializer,
    TimeTrackingModelSerializer,
    UserRegistrationSerializer,
)


class RegisterUserViewSet(GenericViewSet):
    serializer_class = UserRegistrationSerializer
    queryset = None

    def create(self, request: Request) -> Response:
        """Endpoint for registering a user."""

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user = User.objects.get(username=serializer.validated_data["username"])
        refresh: RefreshToken = RefreshToken.for_user(user)

        # Assign the auth tokens after successful registration.
        response = Response(
            {
                "message": "Account succesfully created",
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_201_CREATED,
        )

        return response


class ProjectsViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectsSerializer
    queryset = ProjectsModel.objects.filter(is_deleted=False)

    def destroy(self, request: Request, *args, **kwargs) -> Response:
        """Override method to soft delete the project for archiving purposes."""
        instance: ProjectsModel = self.get_object()

        instance.is_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TimeTrackingsViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TimeTrackingModelSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TimeTrackingModelFilter

    def get_queryset(self):
        """Override get queryset to only filter entries by the authenticated user."""
        request: Request = self.request
        user = request.user

        queryset = TimeTrackingModel.objects.filter(user=user)

        return queryset

    def create(self, request: Request, *args, **kwargs) -> Response:
        """Endpoint to create a Entry"""
        # Override the create method to assign authenticated user to the payload data
        request.data["user"] = request.user.id

        return super().create(request)

    def list(self, request: Request, *args, **kwargs) -> Response:
        """Endpoint to fetch list of entries"""
        # Override the list method to apply filtering.
        queryset = self.filter_queryset(self.get_queryset())

        return Response(
            self.get_serializer(queryset, many=True).data, status.HTTP_200_OK
        )
