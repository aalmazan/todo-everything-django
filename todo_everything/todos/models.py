from django.db import models
from mixins.models import common
from model_utils.models import SoftDeletableModel, TimeStampedModel

from . import tasks


class Todo(
    common.UserStampedModel,
    common.OrganizationStampedModel,
    TimeStampedModel,
    SoftDeletableModel,
    models.Model,
):
    """Main model that contains todo data."""

    title = models.CharField(max_length=100, blank=True)
    body = models.TextField(blank=True)
    completed = models.DateTimeField(null=True, editable=False)

    class Meta:
        db_table = "todo"
        ordering = ["-created"]

    def __str__(self):
        return self.title or "<blank>"

    def save(self, *args, **kwargs):
        tasks.task_todo.delay(self.id)
        return super().save(*args, **kwargs)
