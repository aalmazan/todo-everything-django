from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class UserStampedModel(models.Model):
    """Abstract model that adds which user created the model."""

    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="+")

    class Meta:
        abstract = True
