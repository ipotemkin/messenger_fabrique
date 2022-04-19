from celery import Celery


app = Celery('planner', broker='redis://localhost')


@app.task
def add(x, y):
    return x + y


add.delay(4, 4)
