from django.db import models
from django.db.models import Max
from mixins.models import common
from model_utils.models import SoftDeletableModel, TimeStampedModel

from . import tasks


class Todo(
    common.UserStampedModel,
    common.UserAssignedModel,
    common.OrganizationStampedModel,
    TimeStampedModel,
    SoftDeletableModel,
    models.Model,
):
    """Main model that contains todo data."""

    # local_id = models.PositiveIntegerField(default=1, editable=False)
    title = models.CharField(max_length=100, blank=True)
    body = models.TextField(blank=True)
    completed = models.DateTimeField(null=True, editable=False)
    due_on = models.DateTimeField(null=True, blank=True)
    started_on = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "todo"
        ordering = ["-created"]

    def __str__(self):
        return self.title or "<blank>"

    def get_max_local_id(self):
        """Return the max local id based on the organization or user."""
        if self.organization:
            qs = self.objects.filter(organization=self.organization)
        else:
            qs = self.objects.filter(created_by=self.created_by)
        return qs.aggregate(Max("local_id", default=1)).get("local_id__max")

    def save(self, *args, **kwargs):
        # max_local_id = self.get_max_local_id()
        # self.local_id = max_local_id + 1
        super().save(*args, **kwargs)
        tasks.task_todo.delay(self.id)
