from celery.utils.log import get_task_logger

from reset_schedule.app import config
from reset_schedule.celeryapp import app
from reset_schedule.worker.reschedule_tasks import reschedule
from reset_schedule.worker.test_tasks import print_task, simple_pipeline

logger = get_task_logger(__name__)


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    try:
        if config.is_scheduler():
            return

        app.control.purge()

        tasks_to_remove = ["print_task"]

        tasks_to_schedule = [
            {
                "task": simple_pipeline.pipeline.s().task,
                "name": "simple_pipeline",
                "schedule": 5,
            }
        ]

        reschedule.reschedule_task.apply_async(
            kwargs={
                "tasks_to_remove": tasks_to_remove,
                "tasks_to_schedule": tasks_to_schedule,
                # "tasks_to_reschedule": tasks_to_reschedule
            },
            countdown=5,
        )

    except Exception as e:
        logger.error(f"An exception occurred: {e}")
