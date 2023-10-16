import logging

from celery import shared_task

from . import models

logger = logging.getLogger(__name__)


@shared_task
def task_todo(todo_id: int):
    logger.info("Running todo processor. id=%(id)s", {"id": todo_id})
    todo = models.Todo.objects.get(id=todo_id)
    todo.title = todo.title + " got edited from shared task"
    todo.save()


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)
