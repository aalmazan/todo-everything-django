from django.db import models
from mixins.models import common
from model_utils.models import SoftDeletableModel, TimeStampedModel


class Todo(common.UserStampedModel, TimeStampedModel, SoftDeletableModel, models.Model):
    """Main model that contains todo data."""

    title = models.CharField(max_length=100, blank=True)
    body = models.TextField(blank=True)

    def __str__(self):
        return self.title or "<blank>"
