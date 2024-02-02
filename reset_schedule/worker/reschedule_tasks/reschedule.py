from redbeat import RedBeatScheduler

from reset_schedule.celeryapp import app


def setup_new_schedules():

    redbeat_scheduler = RedBeatScheduler(app=app)

    # schedule = redbeat_scheduler.schedule

    # print(redbeat_scheduler.info)
    print("schedule")
    # print(schedule)
    # print(app.redbeat_conf.schedule)

@app.task(
    # autoretry_for=(Exception,),
    # max_retries=5,
    # default_retry_delay=2,
)
def reschedule_task():
    setup_new_schedules()
