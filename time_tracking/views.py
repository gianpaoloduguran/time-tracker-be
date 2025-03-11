from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from time_tracking.models import ProjectsModel
from time_tracking.serializers import ProjectsSerializer, UserRegistrationSerializer


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

    def destroy(self, request, *args, **kwargs):
        """Override method to soft delete the project for archiving purposes."""
        instance: ProjectsModel = self.get_object()

        instance.is_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
