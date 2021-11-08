import time

from celery import Celery
from celery_dyrygent.tasks import register_workflow_processor
import logging

log = logging.getLogger(__name__)
app = Celery("test", broker="pyamqp://localhost", backend="redis://localhost/0")
app.autodiscover_tasks()
app.conf.result_extended = True
workflow_processor = register_workflow_processor(app)


@app.task
def normal_task():
    log.info("normal task")
    time.sleep(2)


@app.task(throws=(Exception,))
def failing_task():
    log.info("failing task")
    time.sleep(2)
    raise Exception("failure")


@app.task
def callback(msg, *args, **kwargs):
    log.error(f"error called: {msg} {args} {kwargs}")