import factory
from faker import Factory
fake = Factory.create()

from django.contrib.auth.models import User

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User