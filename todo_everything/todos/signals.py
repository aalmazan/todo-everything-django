import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from . import models, tasks

logger = logging.getLogger(__name__)


@receiver(post_save, sender=models.Todo)
def todo_creation(sender, **kwargs):
    logger.info("<signal> Todo creation triggered")
    tasks.notify.delay("todo_created")
