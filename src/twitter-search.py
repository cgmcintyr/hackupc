#!/usr/bin/env python

#-----------------------------------------------------------------------
# twitter-search
#  - performs a basic keyword search for tweets containing the keywords
#    "lazy" and "dog"
#-----------------------------------------------------------------------
import tweepy
from langdetect import detect

from sentiment import get_sentiment
from cities import cities

import config

auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_key, config.access_secret)
api = tweepy.API(auth)

supported_langs = {'en':'English', 'es':'Spanish'}

class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        lang = detect(status.text)

        if lang in supported_langs.keys():
            s = get_sentiment(status.text, supported_langs[lang])
            print("({}) {}".format(s, status.text))

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
myStream.filter(locations=cities['madrid'].bounding)
