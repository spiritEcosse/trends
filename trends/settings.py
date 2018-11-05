import os

CELERY_USE = True
BROKER_URL = 'amqp://user:pass@rabbit//'
CELERY_RESULT_BACKEND = 'redis://redis:6379/1'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/Kiev'

REMOTE_DRIVER = 'http://phantomjs:4444/wd/hub'

RESEARCH = "http://research.picworkflow.com"
MIN_MAX_WORDS = (2, 4)
RATING_MIN = 20
RATING_MAX = 2500

SLEEP_ON_SUBMIT_FORM = 5

DATE_TIME_FORMAT = "%d.%m.%Y %X"

COUNTDOWN = 3
COUNTDOWN_RETRY = 60 * 5
MAX_RETRIES = 10

SHUTTER_IMAGES = -1  # -1: all
SHUTTER_KEYWORDS = 20  # -1: all
SHUTTER_PAGE = 1
SHUTTER_TOKEN = os.environ['SHUTTER_TOKEN']
SHUTTER_PER_PAGE = 100

SPREADSHEET_ID = '1FRbLT1yl0y2q1BnT6dYBVTiyb_sMZl32DupmhczLEuU'
# SPREADSHEET_ID = '13mh0XzQpqGu5oNhRnbg_TaaIpWqYzBEZB51lD_th-RM'
RANGE_NAME = 'A:O'
# How the input data should be interpreted.
VALUE_INPUT_OPTION = 'USER_ENTERED'

# How the input data should be inserted.
INSERT_DATA_OPTION = 'INSERT_ROWS'

SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
