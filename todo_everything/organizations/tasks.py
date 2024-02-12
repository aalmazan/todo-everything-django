import logging

from celery import shared_task

logger = logging.getLogger()


@shared_task
def notify(notification_name: str):
    logger.info("Running task with name %s", notification_name)
