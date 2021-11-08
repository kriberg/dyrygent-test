import time

from celery.canvas import chain
from celery_dyrygent.workflows import Workflow

from .celery import normal_task, failing_task, callback

if __name__ == "__main__":

    chain1 = chain(normal_task.si(), normal_task.si(), failing_task.si())
    chain1.on_error(callback.si(f"Leaf chain 1 failed"))
    chain2 = chain(normal_task.si(), normal_task.si(), failing_task.si())
    chain2.on_error(callback.si(f"Leaf chain 2 failed"))
    chain3 = chain(normal_task.si(), normal_task.si(), failing_task.si())
    chain3.on_error(callback.si(f"Leaf chain 3 failed"))
    master_chain = chain(chain1, chain2, chain3)
    wf = Workflow()
    wf.set_retry_policy("random", 1, 3)
    wf.add_celery_canvas(master_chain)
    result = wf.apply_async(options={"link_error": callback.si("wf error")})
    result.get()
    time.sleep(10)
    master_chain.on_error(callback.si("master error"))
    master_chain.apply_async()
