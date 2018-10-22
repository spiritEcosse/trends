import os

CELERY_USE = True
BROKER_URL = 'amqp://user:pass@rabbit//'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/Kiev'

TOKEN_SHUTTERSTOCK = os.environ['TOKEN_SHUTTERSTOCK']
