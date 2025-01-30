# fintech/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fintech.settings')

app = Celery('fintech')

# Read config from Django settings, use CELERY namespace
app.config_from_object('django.conf:settings', namespace='CELERY')

# Discover tasks in all registered Django app configs
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
