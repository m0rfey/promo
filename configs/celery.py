import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configs.settings')


app = Celery('promo-worker')
app.config_from_object('django.conf.settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {}
