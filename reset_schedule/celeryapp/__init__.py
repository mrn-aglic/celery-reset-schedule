import os

from celery import Celery

from . import celeryconfig
from .celeryconfig import task_queues

app = Celery("reset_schedule")

app.config_from_object(celeryconfig)

instance = os.environ.get("instance")

if instance == "scheduler":
    app.control.purge()
