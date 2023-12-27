from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from model_utils.models import SoftDeletableModel, TimeStampedModel

from .managers import AccountManager


class Account(TimeStampedModel, SoftDeletableModel, AbstractUser):
    """Custom user account class."""

    REQUIRED_FIELDS = []
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"

    # Remove these fields. Names will go to the profile model.
    username = None
    first_name = None
    last_name = None

    email = models.EmailField(_("email address"), unique=True)

    objects = AccountManager()  # type: ignore

    def __str__(self):
        return self.email

    class Meta:
        db_table = "account"

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def has_organization_access(self, organization):
        if isinstance(organization, int):
            filter_q = Q(pk=organization)
        else:
            filter_q = Q(organization=organization)
        return self.organizations.filter(filter_q).exists()


class AccountProfile(TimeStampedModel, SoftDeletableModel, models.Model):
    """Additional info for user accounts."""

    account = models.OneToOneField(
        Account, on_delete=models.CASCADE, related_name="profile"
    )
    full_name = models.TextField(max_length=128, null=True, blank=True)

    def __str__(self):
        return f"{self.account.email} profile"

    class Meta:
        db_table = "account_profile"
