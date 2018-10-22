from __future__ import absolute_import

import itertools

from .celery import app
from .settings import TOKEN_SHUTTERSTOCK

from pytrends.request import TrendReq

from shutterstock.api import ShutterstockAPI

from shutterstock_api.resources import Image


@app.task
def bit_google_trends():
    pytrends = TrendReq(hl='en-US', tz=360)
    trending_searches_df = pytrends.trending_searches()


@app.task
def shutterstock_search():
    Image.API = ShutterstockAPI(token=TOKEN_SHUTTERSTOCK)
    images = Image.list(view='full')

    for image in images:
        stuff = sorted(image.keywords)

        for L in range(0, len(stuff) + 1):
            for subset in itertools.combinations(stuff, L):
                print(subset)
