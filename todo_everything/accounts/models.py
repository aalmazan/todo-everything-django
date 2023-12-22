from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import SoftDeletableModel, TimeStampedModel

from .managers import AccountManager


class Account(AbstractUser):
    """Custom user account class."""

    REQUIRED_FIELDS = []
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"

    username = None
    email = models.EmailField(_("email address"), unique=True)

    objects = AccountManager()  # type: ignore

    def __str__(self):
        return self.email

    class Meta:
        db_table = "account"


class AccountProfile(TimeStampedModel, SoftDeletableModel, models.Model):
    """Additional info for user accounts."""

    account = models.OneToOneField(
        Account, on_delete=models.CASCADE, related_name="profile"
    )
    full_name = models.TextField(max_length=128, null=True, blank=True)

    def __str__(self):
        return "{} profile".format(self.account.email)

    class Meta:
        db_table = "account_profile"
