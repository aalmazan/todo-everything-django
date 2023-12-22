import logging

from celery import shared_task
from rmq.rmq_producer import RMQProducer

logger = logging.getLogger(__name__)

producer = RMQProducer()


@shared_task
def task_todo(todo_id: int):
    logger.info("Running todo processor. id=%(id)s", {"id": todo_id})
    # todo = models.Todo.objects.get(id=todo_id)
    # todo.title = todo.title
    # todo.save()


@shared_task
def notify(notification_name: str):
    logger.info("Todo notify: %s", notification_name)
    producer.publish()
