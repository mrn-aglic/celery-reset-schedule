import redbeat.schedulers
from redbeat import RedBeatScheduler
from redbeat.schedulers import RedBeatSchedulerEntry

from reset_schedule.celeryapp import app
from reset_schedule.worker.helper_functions import get_schedules, log_schedule_execution


def get_redbeat_key_prefix():
    key_prefix = app.redbeat_conf.key_prefix
    return key_prefix.split(":")[0]


@app.task(bind=True)
def print_schedule(self):
    schedules = get_schedules()
    print(schedules)

    log_schedule_execution(self)


@app.task(bind=True)
def remove_periodic_tasks(self, task_names: list[str]):
    redbeat_scheduler = RedBeatScheduler(app=app)

    key_prefix = get_redbeat_key_prefix()

    for task in task_names:
        key = f"{key_prefix}:{task}"
        entry = redbeat_scheduler.Entry.from_key(key=key, app=app)
        entry.delete()

    log_schedule_execution(self)


@app.task(bind=True)
def schedule_periodic_tasks(self, tasks: list[dict]):
    redbeat_scheduler = redbeat.RedBeatScheduler(app=app)

    entries = {}

    for task_details in tasks:
        schedule = task_details["schedule"]
        task = task_details["task"]
        name = task_details["name"]

        entries[name] = RedBeatSchedulerEntry(name, task, schedule, app=app)

    redbeat_scheduler.update_from_dict(entries)

    log_schedule_execution(self)


@app.task
def reschedule_task(tasks_to_remove: list[str], tasks_to_schedule: list[dict]):
    return (
        print_schedule.s()
        | remove_periodic_tasks.si(task_names=tasks_to_remove)
        | schedule_periodic_tasks.si(tasks=tasks_to_schedule)
        | print_schedule.si()
    ).apply_async()
