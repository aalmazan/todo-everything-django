from celery import shared_task

from . import models


@shared_task
def task_todo(todo_id):
    print("Running task...", todo_id)
    todo = models.Todo.objects.get(todo_id)
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
