import os
import sys
from pathlib import Path

from celery import Celery

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Add path to main project dir. Prevents import errors due to missing PATHs
sys.path.insert(0, os.path.dirname(os.path.join(BASE_DIR)))
# sys.path.append(os.path.abspath(".."))

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "todo_everything.settings")

app = Celery("todo_everything")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.

app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()
