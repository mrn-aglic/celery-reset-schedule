from reset_schedule.celeryapp import app
from reset_schedule.worker.helper_functions import log_schedule_execution


@app.task(bind=True)
def printer(self):
    print("Hello from printer :-)")
    log_schedule_execution(self)


@app.task
def pipeline():
    return printer.s().apply_async()
