import json
from datetime import datetime

import redbeat.schedulers
from celery import Task
from redbeat import RedBeatSchedulerEntry
from redbeat.schedulers import RedBeatConfig

from reset_schedule.celeryapp import app


def get_schedules() -> dict:
    config = RedBeatConfig(app)

    schedule_key = config.schedule_key

    redis = redbeat.schedulers.get_redis(app)

    elements = redis.zrange(schedule_key, 0, -1, withscores=False)

    entries = {el: RedBeatSchedulerEntry.from_key(key=el, app=app) for el in elements}

    return entries


def get_definition(entry: RedBeatSchedulerEntry) -> dict:
    return {
        "name": entry.name,
        "task": entry.task,
        "args": entry.args,
        "kwargs": entry.kwargs,
        "options": entry.options,
        "schedule": str(entry.schedule),
        "enabled": entry.enabled,
    }


def log_schedule_execution(task: Task):
    schedule = get_schedules()

    name = str(task)

    d_schedule = {}
    for key in schedule:
        d_schedule[key] = get_definition(schedule[key])

    with open("logs.txt", "a") as file:
        data = {
            "time": datetime.utcnow().isoformat(),
            "task": name,
            "schedule": d_schedule,
        }
        json.dump(data, fp=file, indent=4, sort_keys=True)
        file.write("\n")
