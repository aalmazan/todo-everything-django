from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Max
from django.utils import timezone
from mixins.models import common
from model_utils.models import (
    SoftDeletableManager,
    SoftDeletableModel,
    TimeStampedModel,
)

from . import tasks

Account = get_user_model()


class TodoManager(SoftDeletableManager):
    def completed(self):
        return self.get_queryset().filter(completed__isnull=False)

    def not_completed(self):
        return self.get_queryset().filter(completed__isnull=True)

    def unassigned(self):
        return self.get_queryset().filter(assigned_to__isnull=True)

    def assigned(self):
        return self.get_queryset().filter(assigned_to__isnull=False)

    def for_org(self, organization=None, user=None):
        qs = self.get_queryset()
        if organization:
            return qs.filter(organization=organization)
        elif user and not organization:
            orgs = user.organizations.all()
            return qs.filter(organization__in=orgs)
        else:
            raise ValueError("One of `organization` or `user` is required")

    def for_user(self, user: Account):
        return self.get_queryset().filter(created_by=user)

    def due_today(self):
        return self.get_queryset().filter(
            due_on__gte=timezone.now().replace(hour=0, minute=0, second=0),
            due_on__lte=timezone.now().replace(hour=23, minute=59, second=59),
        )

    def started_not_done(self):
        return self.get_queryset().filter(
            started_on__isnull=False, completed__isnull=True
        )


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
    todos = TodoManager()

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
