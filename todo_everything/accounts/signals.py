from logging import getLogger

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from . import models, tasks

logger = getLogger(__name__)


@receiver(pre_save, sender=models.Account)
def pre_account_creation(sender, **kwargs):
    logger.info("Account creation about to happen")
    tasks.notify.delay("pre_account_create")


@receiver(post_save, sender=models.Account)
def create_profile(sender, **kwargs):
    instance = kwargs.pop("instance", None)
    created = kwargs.pop("created", False)
    full_name = kwargs.pop("full_name", "")

    logger.info("Account creation triggered")
    tasks.notify.delay("account_created")

    if created:
        models.AccountProfile.objects.create(account=instance, full_name=full_name)
