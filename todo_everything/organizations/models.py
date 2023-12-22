from accounts import models as accounts_models
from django.db import models
from model_utils.models import SoftDeletableModel, TimeStampedModel


class Organization(TimeStampedModel, SoftDeletableModel, models.Model):
    """Organization model mainly to group `Account`s."""

    name = models.CharField(max_length=64)
    accounts = models.ManyToManyField(
        accounts_models.Account,
        through="OrganizationAccounts",
        through_fields=("organization", "account"),
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class OrganizationAccounts(TimeStampedModel, models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    account = models.ForeignKey(accounts_models.Account, on_delete=models.CASCADE)
    # TODO: Add meta things like group, person, inviter (from Django example).
