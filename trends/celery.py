from __future__ import absolute_import
from celery import Celery
from kombu import Exchange
from kombu import Queue

app = Celery('trends')
app.config_from_object('trends.settings')
app.autodiscover_tasks(('trends', ), force=True)

app.conf.update(
    {
        'CELERY_QUEUES': (
            Queue('shutterstock_search', Exchange('shutterstock_search'),
                  routing_key='trends.tasks.shutterstock_search'),
            Queue('combinations', Exchange('combinations'), routing_key='trends.tasks.combinations'),
            Queue('research_task', Exchange('research_task'), routing_key='trends.tasks.research_task'),
            Queue('write_to_google', Exchange('write_to_google'), routing_key='trends.tasks.write_to_google'),
        ),
        'CELERY_ROUTES': {
            'trends.tasks.shutterstock_search': {
                'queue': 'shutterstock_search',
                'routing_key': 'trends.tasks.shutterstock_search',
            },
            'trends.tasks.combinations': {
                'queue': 'combinations',
                'routing_key': 'trends.tasks.combinations',
            },
            'trends.tasks.research_task': {
                'queue': 'research_task',
                'routing_key': 'trends.tasks.research_task',
            },
            'trends.tasks.write_to_google': {
                'queue': 'write_to_google',
                'routing_key': 'trends.tasks.write_to_google',
            },
        },
        'CELERY_DEFAULT_QUEUE': 'celery',
        'CELERY_DEFAULT_EXCHANGE': 'celery',
        'CELERY_DEFAULT_ROUTING_KEY': 'celery',
    }
)
