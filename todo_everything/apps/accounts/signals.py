from django.db.models.signals import post_save
from django.dispatch import receiver

from . import models


@receiver(post_save, sender=models.Account)
def create_profile(sender, **kwargs):
    instance = kwargs.pop("instance", None)
    created = kwargs.pop("created", False)
    full_name = kwargs.pop("full_name", "")

    if created:
        models.AccountProfile.objects.create(account=instance, full_name=full_name)
