import factory

from . import models


class AccountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Account

    email = factory.Faker("email")


class AccountProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.AccountProfile

    account = factory.SubFactory(AccountFactory)
    full_name = factory.Faker("name")
