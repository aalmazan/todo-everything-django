from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from organizations import models as organizations_model


# https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.SET
def get_sentinel_organization():
    return organizations_model.Organization.objects.get_or_create(
        name=settings.get("DEFAULT_SENTINEL_ORGANIZATION")
    )[0]


# https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.SET
def get_sentinel_user():
    return get_user_model().objects.get_or_create(
        email=settings.get("DEFAULT_SENTINEL_USER_EMAI")
    )[0]


class UserStampedModel(models.Model):
    """Abstract model that adds which user created the model."""

    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET(get_sentinel_user),
        related_name="+",
    )

    class Meta:
        abstract = True


class OrganizationStampedModel(models.Model):
    """Abstract model that adds which org is assigned to the model."""

    # TODO: Does this belong in `mixins.models.common` or within the organizations app?

    organization = models.ForeignKey(
        organizations_model.Organization,
        on_delete=models.SET(get_sentinel_organization),
        related_name="+",
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True
