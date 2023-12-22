from django.contrib.auth import get_user_model
from django.db import models


class UserStampedModel(models.Model):
    """Abstract model that adds which user created the model."""

    created_by = models.ForeignKey(
        get_user_model(), on_delete=models.SET_DEFAULT, related_name="+", default=1
    )

    class Meta:
        abstract = True
