from __future__ import absolute_import

import itertools

import time

from pytrends.request import TrendReq
from selenium import webdriver
from selenium.common import exceptions
from shutterstock.api import ShutterstockAPI
from shutterstock_api.resources import Image
from trends.celery import app
from trends import settings
from celery import group


@app.task
def bit_google_trends():
    pytrends = TrendReq(hl='en-US', tz=360)
    trending_searches_df = pytrends.trending_searches()


@app.task
def shutterstock_search():
    Image.API = ShutterstockAPI(token=settings.TOKEN_SHUTTERSTOCK)
    [combinations.delay('/'.join(set(image.keywords[:settings.SHUTTER_KEYWORDS])))
     for image in Image.list(view='full')[:settings.SHUTTER_IMAGES]]


@app.task(countdown=settings.COUNTDOWN)
def combinations(keywords):
    keywords = keywords.split('/')
    for comb in range(*settings.MIN_MAX_WORDS):
        [research.delay(' '.join(subset)) for subset in itertools.combinations(keywords, comb)]


@app.task(countdown=settings.COUNTDOWN)
def research(subject):
    data = {'subject': subject}
    driver = webdriver.Remote(
        command_executor=settings.REMOTE_DRIVER,
        desired_capabilities={'browserName': 'firefox'},
    )
    driver.get(settings.RESEARCH)

    time.sleep(1)

    elem = driver.find_element_by_id("search")
    elem.send_keys(subject)
    elem.submit()

    time.sleep(3)

    try:
        ready = driver.find_element_by_xpath("//tr[@recent='true']//strong")
    except exceptions.NoSuchElementException:
        pass
    else:
        rating = float(ready.text)
        data['rating'] = rating
        if settings.RATING_MIN < rating < settings.RATING_MAX:
            data['excellent'] = True
    finally:
        driver.quit()
        return data
