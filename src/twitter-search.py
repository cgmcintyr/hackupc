#!/usr/bin/env python
"""Core twitter search stuff"""

import tweepy
from langdetect import detect
from collections import namedtuple

from sentiment import get_sentiment, supported_langs
from cities import cities

import config

auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_key, config.access_secret)
api = tweepy.API(auth)

HappyMapTweet = namedtuple('HappyMapTweet', 
                           ['city', 'latitdue', 'longitude', 'sentiment', 'text'])

def this_method_should_do_something(data):
    print(data)

class CityStreamListener(tweepy.StreamListener):
    def __init__(self, city, limit):
        self.city = city.name
        self.latitude = city.latitude
        self.longitude = city.longitude

        self.status_count = 0
        self.status_stop_count = limit

    def on_status(self, status):
        lang = None

        try:
            lang = detect(status.text)
        except LangDetectException:
            pass

        if lang in supported_langs.keys():
            self.status_count += 1
            s = get_sentiment(status.text, supported_langs[lang])
            h = HappyMapTweet(self.city, self.latitude, self.longitude, s, status.text)
            this_method_should_do_something(h)

        if self.status_stop_count == self.status_count:
            return False

while True:
    for _, city in cities.items():
        print(city)
        myStreamListener = CityStreamListener(city, 3)
        myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
        myStream.filter(locations=city.bounding)
