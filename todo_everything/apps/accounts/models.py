from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import AccountManager


class Account(AbstractUser):
    """Custom user account class."""

    REQUIRED_FIELDS = []
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"

    username = None
    email = models.EmailField(_("email address"), unique=True)

    objects = AccountManager()

    class Meta:
        db_table = "account"


class AccountProfile(models.Model):
    """Additional info for user accounts."""

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    full_name = models.TextField(max_length=128)
