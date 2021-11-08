import time

from celery.canvas import chain
from celery_dyrygent.workflows import Workflow

from .celery import normal_task, failing_task, callback

if __name__ == "__main__":

    chain1 = chain(normal_task.si(), normal_task.si(), failing_task.si())
    chain1.on_error(callback.si(f"Leaf chain 1 failed"))
    wf = Workflow()
    wf.set_retry_policy("random", 1, 3)
    wf.add_celery_canvas(chain1)
    result = wf.apply_async(options={"link_error": callback.si("wf error")})
    result.get()
    time.sleep(10)
    chain1.on_error(callback.si("master error"))
    chain1.apply_async()
