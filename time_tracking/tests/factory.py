import factory

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from time_tracking.models import ProjectsModel, TimeTrackingModel


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")

    @classmethod
    def create(cls, **kwargs):
        """Override to handle custom create process to mimic original create user flow"""
        password = kwargs.get("password")
        kwargs.update({"password": make_password(password)})
        new_user = super().create(**kwargs)

        return new_user


class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProjectsModel

    title = factory.Faker("name")


class TimeTrackingModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TimeTrackingModel

    work_description = factory.Faker("sentence")
