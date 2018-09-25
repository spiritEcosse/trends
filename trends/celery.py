from __future__ import absolute_import
from celery import Celery

app = Celery('trends', broker='amqp://user:pass@rabbit//')
app.autodiscover_tasks(('trends', ))
