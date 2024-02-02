from celery.schedules import crontab
from celery.utils.log import get_task_logger
from redbeat import RedBeatSchedulerEntry

from reset_schedule.app import config
from reset_schedule.celeryapp import app
from reset_schedule.worker.test_tasks import (
    print_task,
    simple_pipeline,
)

logger = get_task_logger(__name__)


if config.is_dev():
    import logging
    logging.basicConfig(level=logging.INFO)


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    try:

        logger.info("SETUP PERIODIC TASK")

        # print_s = print_task.pipeline.s().stamp(header="print_task")
        #
        # logger.info("print_s")
        # logger.info(print_s)
        # logger.info(dir(print_s))
        # logger.info(print_s.stamp_links)
        # logger.info(print_s.options)

        sender.add_periodic_task(
            5,
            print_task.pipeline.s(),
            name="print_task"
        )
        sender.add_periodic_task(
            2,
            simple_pipeline.pipeline.s(),
            name="simple_pipeline2"
        )

        app.conf.beat_schedule = {
            "example": {
                "task": print_task.pipeline.s().name,
                "schedule": 4
            }
        }

        # interval = celery.schedules.schedule(run_every=60)  # seconds
        # entry = RedBeatSchedulerEntry('task-name', print_task.pipeline.s().task, crontab(minute="*"),  app=sender)
        entry = RedBeatSchedulerEntry('task-name', print_task.pipeline.s().task, 2,  app=sender)
        entry.save()

    except Exception as e:
        logger.error(f"An exception occurred: {e}")

