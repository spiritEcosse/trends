from __future__ import absolute_import
from trends.celery import app
from pytrends.request import TrendReq


@app.task
def bit_google_trends():
    pytrends = TrendReq(hl='en-US', tz=360)
    kw_list = ["Blockchain"]
    pytrends.build_payload(kw_list, cat=0, timeframe='today 5-y', geo='', gprop='')
