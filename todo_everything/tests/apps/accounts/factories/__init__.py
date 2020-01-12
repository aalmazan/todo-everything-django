import factory
from faker import Factory as FakerFactory

faker = FakerFactory.create()


class AccountFactory(factory.django.DjangoModelFactory):
    """Factory to create custom user Account instances."""

    class Meta:
        model = "accounts.Account"
