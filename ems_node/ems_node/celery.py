import os
from celery import Celery
from celery.schedules import crontab


# set the default Django settings module for the 'celery' program
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ems_node.settings")

app = Celery('ems_node')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


app.conf.beat_schedule = {
    'record-node-every-5-minutes': {
        'task': 'record_node_state',
        'schedule': crontab(minute='*/5'),
    },
    # 'record-node-every-10-seconds': {
    #     'task': 'record_node_state',
    #     'schedule': 10.0,
    # },
    # 'add-every-30-seconds': {
    #     'task': 'tasks.add',
    #     'schedule': 30.0,
    #     'args': (16, 16)
    # },
}

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

