#!/usr/bin/env python

import json
import tweepy
from tweepy import OAuthHandler
from tweepy import Stream, API, StreamListener
from config import *

from cities import bounding

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = API(auth)

class MyStreamListener(tweepy.StreamListener):
    def on_data(self, data):
        tweet = json.loads(data)

        tweetid = tweet.get('id', None)
        place = tweet.get('place', None)
        user = tweet['user']['name'] if tweet.get('user', None) is not None else None
        text = tweet.get('text', None)

        print("({}) {}: {} [from {}]".format(tweetid, user, text, place))

stream = Stream(auth, MyStreamListener())
stream.filter(locations=bounding['spain'])
