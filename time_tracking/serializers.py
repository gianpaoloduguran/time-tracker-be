from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Q
from django.utils import timezone

from rest_framework import serializers

from time_tracking.models import ProjectsModel, TimeTrackingModel


class UserRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={"input_type": "password"},
        error_messages={
            "blank": "This field is required",
            "null": "This field is required",
        },
    )

    class Meta:
        model = User
        fields = ["password", "username"]
        extra_kwargs = {
            "username": {
                "error_messages": {
                    "blank": "This field is required",
                    "null": "This field is required",
                },
            },
        }

    def validate_username(self, value):
        """Validate the username if the given value is already taken."""
        lower_email = value.lower()
        if User.objects.filter(
            Q(email__iexact=lower_email) | Q(username__iexact=lower_email)
        ).exists():
            raise serializers.ValidationError(
                "This email/username has already been taken."
            )

        return lower_email

    def validate(self, attrs):
        """
        If username was given, check for password, and vice-versa for the
        password.
        """
        validation_errors = {}

        if attrs.get("username") and not attrs.get("password"):
            validation_errors["password"] = "This field is required."
        elif not attrs.get("report") and not attrs.get("username"):
            validation_errors["username"] = "This field is required."
            if not attrs.get("password"):
                validation_errors["password"] = "This field is required."

        if validation_errors:
            raise serializers.ValidationError(validation_errors)

        return attrs

    def create(self, validated_data):
        """Finalize Registration of Customer user"""
        with transaction.atomic():
            password = validated_data.pop("password")
            username = validated_data.pop("username")
            # user = self.context.get("user")
            user = User.objects.create_user(
                username=username,
                email=username,
            )
            user.set_password(password)
            user.save()

            return user


class ProjectsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectsModel
        fields = ["id", "title"]

    def validate_title(self, value):
        """Validate the username if the given value is already taken."""
        if ProjectsModel.objects.filter(title__exact=value).exists():
            raise serializers.ValidationError("Project title is already taken.")

        return value


class TimeTrackingModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeTrackingModel
        fields = [
            "id",
            "project",
            "user",
            "date_worked",
            "work_description",
            "hours",
            "project_title",
            "created_at",
            "updated_at",
        ]
