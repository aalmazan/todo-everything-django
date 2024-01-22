from logging import getLogger

from accounts import models as accounts_models
from django.db.models.signals import post_save
from django.dispatch import receiver

from . import models, tasks

logger = getLogger(__name__)


@receiver(post_save, sender=accounts_models.Account)
def create_organization(sender, **kwargs):
    instance: accounts_models.Account | None = kwargs.pop("instance", None)
    created = kwargs.pop("created", False)

    logger.info("Account creation triggered, create_org")
    tasks.notify.delay("create_organization")

    if created and instance:
        logger.info("Creating with instance: %s %s", instance.email, instance.full_name)
        organization = models.Organization.objects.create(
            name=instance.full_name, is_self_org=True
        )
        logger.info("Org created: %s", organization.name)
        models.OrganizationAccount.objects.create(
            organization=organization,
            account=instance,
            role=models.ORGANIZATION_ADMIN,
        )
