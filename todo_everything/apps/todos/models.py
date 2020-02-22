from django.db import models
from model_utils.models import SoftDeletableModel, TimeStampedModel
from todo_everything.mixins.models import common


class Todo(common.UserStampedModel, TimeStampedModel, SoftDeletableModel, models.Model):
    """Main model that contains todo data."""

    title = models.CharField(max_length=100, blank=True)
    body = models.TextField(blank=True)
