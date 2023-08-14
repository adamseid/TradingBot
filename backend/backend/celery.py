import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('backend')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

PERIOD = 5.0

app.conf.beat_schedule = {
    'update-raw': {
        'task': 'updateRaw',
        'schedule': PERIOD,
    },
    'update-analysis': {
        'task': 'updateAnalysis',
        'schedule': PERIOD,
    },
    'update-frontend': {
        'task': 'updateFrontend',
        'schedule': PERIOD,
    },
    'update-simulation': {
        'task': 'updateSimulation',
        'schedule': PERIOD,
    }
}
