from __future__ import absolute_import
from celery import Celery

app = Celery('trends')
app.config_from_object('trends.settings')
app.autodiscover_tasks(('trends', ))
