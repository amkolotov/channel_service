import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'update_rates': {
        'task': 'main.tasks.update_rates_from_cbr',
        'schedule': 60*1,
        'args': (),
    },
    'get_data_from_gs': {
        'task': 'main.tasks.get_data_from_gs_save_in_db',
        'schedule': 60*1,
        'args': (),
    }
}