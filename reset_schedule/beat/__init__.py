from celery.schedules import crontab
from celery.utils.log import get_task_logger
from redbeat import RedBeatSchedulerEntry

from reset_schedule.app import config
from reset_schedule.celeryapp import app
from reset_schedule.worker.helper_functions import get_schedules
from reset_schedule.worker.test_tasks import print_task, simple_pipeline

logger = get_task_logger(__name__)

if config.is_dev():
    import logging

    logging.basicConfig(level=logging.INFO)


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    try:
        logger.info("SETUP PERIODIC TASK")

        entry1 = RedBeatSchedulerEntry(
            "print_task", print_task.pipeline.s().task, 20, app=app
        )

        entry2 = RedBeatSchedulerEntry(
            "simple_pipeline",
            simple_pipeline.pipeline.s().task,
            # 15,
            crontab(minute="0"),
            app=app,
        )

        entry1.save()
        entry2.save()

        logger.info(get_schedules())

    except Exception as e:
        logger.error(f"An exception occurred: {e}")
