import factory
from accounts.factories import AccountFactory

from . import models


class TodoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Todo

    title = factory.Faker("sentence")
    body = factory.Faker("paragraph")
    completed = None
    created_by = factory.SubFactory(AccountFactory)
