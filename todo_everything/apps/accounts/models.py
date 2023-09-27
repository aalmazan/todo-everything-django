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
