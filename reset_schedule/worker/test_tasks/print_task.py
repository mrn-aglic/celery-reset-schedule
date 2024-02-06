from reset_schedule.celeryapp import app
from reset_schedule.worker.helper_functions import log_schedule_execution


@app.task(bind=True)
def printer(self, task_arg):
    print(task_arg)
    log_schedule_execution(self)


@app.task
def some_task(*arg, a=None, b=None, c=None):
    print(f"print task args: a: {a}, b: {b}, c: {c}")


@app.task
def pipeline():
    return printer.s(some_task.s([1, 2, 3], a=15)).apply_async()
