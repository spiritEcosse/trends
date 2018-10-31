"""
    get populated images from shutterstock
    check them in research
    write better results in google spreadsheets
"""
from __future__ import absolute_import

import itertools

import time

from datetime import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import client
from oauth2client import file
from oauth2client import tools
from pprint import pprint
from pytrends.request import TrendReq
from redis import StrictRedis
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from shutterstock.api import ShutterstockAPI
from shutterstock_api.resources import Image
from trends import settings
from trends.celery import app


def get_webdriver():
    return webdriver.Remote(
        command_executor=settings.REMOTE_DRIVER,
        desired_capabilities=DesiredCapabilities.PHANTOMJS,
    )


def image_key_order():
    return ('description', 'image_type', 'categories', 'is_illustration', 'original_filename', 'url', 'id')


def research_key_order():
    return ('0', '1', '2', '3', '4', '5')


def image_attr(image):
    return {
        "description": image.description,
        "image_type": image.image_type,
        "categories": ', '.join([category['name'] for category in image.categories]),
        "is_illustration": image.is_illustration,
        "original_filename": image.original_filename,
        "url": image.assets['huge_thumb']['url'],
        "id": image.id,
    }


def research_data_dict(tds):
    return dict([(key, td.text) for key, td in enumerate(tds[:6])])


@app.task
def bit_google_trends():
    pytrends = TrendReq(hl='en-US', tz=360)
    [research_task.delay(subject) for subject in pytrends.trending_searches().title]


@app.task
def shutterstock_search():
    Image.API = ShutterstockAPI(token=settings.SHUTTER_TOKEN)
    for image in Image.list(view='full', per_page=settings.SHUTTER_PER_PAGE,
                            page=settings.SHUTTER_PAGE)[:settings.SHUTTER_IMAGES]:
        keywords = []

        for word in image.keywords[:settings.SHUTTER_KEYWORDS]:
            keywords.extend(word.split(' '))

        combinations.delay('/'.join(set(keywords)), image_attr(image))


@app.task(countdown=settings.COUNTDOWN)
def combinations(keywords, image):
    keywords = keywords.split('/')
    for comb in range(*settings.MIN_MAX_WORDS):
        [research_task.delay(' '.join(subset), image) for subset in itertools.combinations(keywords, comb)]


@app.task(bind=True, countdown=settings.COUNTDOWN)
def research_task(self, subject, image={}):
    data = {'subject': subject}

    try:
        driver = get_webdriver()
        driver.get(settings.RESEARCH)

        time.sleep(1)

        try:
            elem = driver.find_element_by_id("search")
        except exceptions.NoSuchElementException as exc:
            raise self.retry(countdown=settings.COUNTDOWN_RETRY, exc=exc, max_retries=settings.MAX_RETRIES)

        elem.send_keys(subject)
        elem.submit()

        time.sleep(settings.SLEEP_ON_SUBMIT_FORM)

        try:
            ready = driver.find_element_by_xpath("//tr[@recent='true']")
        except exceptions.NoSuchElementException as exc:
            raise self.retry(countdown=settings.COUNTDOWN_RETRY, exc=exc, max_retries=settings.MAX_RETRIES)
        else:
            rating = float(ready.find_element_by_tag_name('strong').text)
            data['rating'] = rating

            research_data = ready.find_elements_by_tag_name('td')
            redis = StrictRedis(host='redis')

            print(
                'redis.sismember("keywords", research_data[0])',
                redis.sismember(
                    "keywords",
                    research_data[0]), research_data[0])

            if settings.RATING_MIN < rating < settings.RATING_MAX and not redis.sismember("keywords", research_data[
                    0]):
                data['write_to_google'] = True
                write_to_google.delay(subject, image, research_data_dict(research_data))
        finally:
            driver.quit()
            return data
    except exceptions.WebDriverException as exc:
        raise self.retry(countdown=settings.COUNTDOWN_RETRY, exc=exc, max_retries=settings.MAX_RETRIES)


@app.task
def write_to_google(subject, image, research_dict):
    store = file.Storage('token.json')
    creds = store.get()

    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', settings.SCOPES)
        creds = tools.run_flow(flow, store)

    service = build('sheets', 'v4', http=creds.authorize(Http()), cache_discovery=False)

    image_data = []
    if image:
        for key in image_key_order():
            image_data.append(image[key])

    research_data = []
    for key in research_key_order():
        research_data.append(research_dict[key])

    value_range_body = {
        "majorDimension": "ROWS",
        'values': [
            [datetime.now().strftime(settings.DATE_TIME_FORMAT), subject] + research_data + image_data
        ],
    }

    request = service.spreadsheets().values().append(
        spreadsheetId=settings.SPREADSHEET_ID,
        range=settings.RANGE_NAME,
        valueInputOption=settings.VALUE_INPUT_OPTION,
        insertDataOption=settings.INSERT_DATA_OPTION,
        body=value_range_body
    )
    response = request.execute()
    pprint(response)

    redis = StrictRedis(host='redis')
    redis.sadd("keywords", research_data[0])
    redis.save()
    print('redis.add("keywords", research_data[0])', research_data[0])
