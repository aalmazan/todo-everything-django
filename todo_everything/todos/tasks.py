import logging

from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task
def task_todo(todo_id: int):
    logger.info("Running todo processor. id=%(id)s", {"id": todo_id})
    # todo = models.Todo.objects.get(id=todo_id)
    # todo.title = todo.title
    # todo.save()
