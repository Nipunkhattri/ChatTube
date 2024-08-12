from celery import Celery
from celery_tasks.config import CELERY_TASK, CELERY_BEAT_SCHEDULE

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config["CELERY_RESULT_BACKEND"],
        broker=app.config["CELERY_BROKER_URL"],
    )

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    celery.conf.beat_schedule = CELERY_BEAT_SCHEDULE
    celery.autodiscover_tasks(CELERY_TASK)

    return celery