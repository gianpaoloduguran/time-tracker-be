import factory

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User


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
