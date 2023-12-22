from django.db import models
from django.utils import timezone
from mixins.models import common
from model_utils.models import SoftDeletableModel, TimeStampedModel

from . import tasks


class Todo(common.UserStampedModel, TimeStampedModel, SoftDeletableModel, models.Model):
    """Main model that contains todo data."""

    title = models.CharField(max_length=100, blank=True)
    body = models.TextField(blank=True)
    completed = models.DateTimeField(null=True, editable=False)

    def __str__(self):
        return self.title or "<blank>"

    def complete(self, commit=True):
        self.completed = timezone.now()
        if commit:
            self.save(update_fields=["completed"])
        return self

    def uncomplete(self, commit=True):
        self.completed = None
        if commit:
            self.save(update_fields=["completed"])
        return self

    def save(self, *args, **kwargs):
        tasks.task_todo.delay(self.id)
        return super().save(*args, **kwargs)
