from django.db import models
from model_utils.models import SoftDeletableModel, TimeStampedModel


class Organization(TimeStampedModel, SoftDeletableModel, models.Model):
    """Organization model mainly to group `Account`s."""

    name = models.CharField(max_length=64)
