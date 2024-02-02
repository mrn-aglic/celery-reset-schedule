from celery.utils.log import get_task_logger
from reset_schedule.celeryapp import app
from reset_schedule.worker.reschedule_tasks import reschedule
from reset_schedule.worker.test_tasks import (
    print_task,
    simple_pipeline,
)

logger = get_task_logger(__name__)


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    try:
        logger.info("Send some messages")

        reschedule.reschedule_task.apply_async(countdown=12)
        # reschedule.reschedule_task.apply_async(countdown=5)

    except Exception as e:
        logger.error(f"An exception occurred: {e}")
