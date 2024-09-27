"""
Provides factory for Customer.
"""
from django.contrib.auth.models import User  # Replace this with the actual Customer model
import factory
from factory.django import DjangoModelFactory

from brands.models import Brand  # Replace this with the actual Brand model


class CustomerFactory(DjangoModelFactory):
    """ Customer creation factory."""
    class Meta:
        model = User  # Replace this with the actual Customer model
        django_get_or_create = ('email', 'username')

    username = factory.Sequence(lambda arg: f'customer{arg}')
    email = factory.Sequence(lambda arg: f'customer+test+{arg}@example.com')
    password = factory.PostGenerationMethodCall('set_password', 'test')
    first_name = factory.Sequence(lambda arg: f'Customer{arg}')
    last_name = 'Test'
    is_active = True


class BrandFactory(DjangoModelFactory):
    """ Brand creation factory."""
    class Meta:
        model = Brand  # Replace this with the actual Brand model

    name = factory.Sequence(lambda arg: f'brand name {arg}')
    short_name = factory.Sequence(lambda arg: f'brand{arg}')
    description = factory.Sequence(lambda arg: f'description{arg}')
    logo = None
    active = True
