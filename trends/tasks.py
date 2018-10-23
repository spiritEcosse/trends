from __future__ import absolute_import

import itertools

from trends.celery import app
from trends.settings import TOKEN_SHUTTERSTOCK

from pytrends.request import TrendReq

from shutterstock.api import ShutterstockAPI

from shutterstock_api.resources import Image

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


@app.task
def bit_google_trends():
    pytrends = TrendReq(hl='en-US', tz=360)
    trending_searches_df = pytrends.trending_searches()


@app.task
def shutterstock_search():
    Image.API = ShutterstockAPI(token=TOKEN_SHUTTERSTOCK)
    images = Image.list(view='full')

    driver = webdriver.Remote(
        command_executor='http://firefox:4444/wd/hub',
        desired_capabilities={'browserName': 'firefox'},
    )
    driver.get("http://research.picworkflow.com")
    elem = driver.find_element_by_id("search")

    for image in images:
        stuff = sorted(image.keywords)

        for L in range(0, len(stuff) + 1):
            for subset in itertools.combinations(stuff, L):
                elem.send_keys(' '.join(subset))
                element.submit()
