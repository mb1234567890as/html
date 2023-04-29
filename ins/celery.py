import os
from celery import Celery


from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ins.settings")

app = Celery("ins")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
app.conf.timezone = "Asia/Bishkek"

app.conf.beat_schedule = {
    "add-every-5-seconds": {
        "task": "dbins.tasks.create_random_user_accounts",
        "schedule": crontab(minute='*/1'),
        "args": (2,),
    },
}
