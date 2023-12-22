from django.contrib.auth import get_user_model
from django.db import models
from model_utils.models import SoftDeletableModel, TimeStampedModel


class Organization(TimeStampedModel, SoftDeletableModel, models.Model):
    """Organization model mainly to group `Account`s."""

    name = models.CharField(max_length=64)
    accounts = models.ManyToManyField(
        get_user_model(),
        through="OrganizationAccounts",
        through_fields=("organization", "account"),
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class OrganizationAccounts(TimeStampedModel, models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    account = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    # TODO: Add meta things like group, person, inviter (from Django example).
