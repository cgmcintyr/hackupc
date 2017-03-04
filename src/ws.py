#!/usr/bin/env python

import traceback
import sys

import gevent
import gevent.monkey
gevent.monkey.patch_all()

from geventwebsocket.handler import WebSocketHandler
from gevent import pywsgi

import random

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream, API
import json

import tweepy
from langdetect import detect
from collections import namedtuple

from cities import bounding
from config import *
from sentiment import get_sentiment, supported_langs

Tweet = namedtuple('Tweet', ['id', 'place', 'user', 'text', 'sentiment'])

class MyStreamListener(StreamListener):
    def __init__(self):
        self.sockets = []
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_key, access_secret)
        self.api = API(auth)
        self.stream = Stream(auth, self)

    def add_socket(self, ws):
        self.sockets.append(ws)

    def run(self):
        try:
            self.stream.filter(locations=bounding['spain'])
        except Exception:
            self.stream.disconnect()

    def start(self):
        gevent.spawn(self.run)

    def send(self, ws, data):
        try:
            ws.send(data.encode('utf-8'))
        except Exception:
            # the web socket die..
            self.sockets.remove(ws)


    def on_data(self, data):
        print("data")
        tweet = json.loads(data)

        tweetid = tweet.get('id', None)
        place = tweet.get('place', None)
        user = tweet['user']['name'] if tweet.get('user', None) is not None else None
        text = tweet.get('text', None)
        lang = None

        try:
            lang = detect(text)
        except LangDetectException:
            pass

        if lang in supported_langs.keys():
            s = get_sentiment(status.text, supported_langs[lang])
            tweet = Tweet(tweetid, place, user, text, s)
            print(h)
            for ws in self.sockets:
                data = json.dumps(h.__dict__).encode('utf-8')
                gevent.spawn(self.send, ws, data)
        else:
            print("detected lang '{}' is not supported".format(lang))

        return True

    def on_error(self, status):
        print("Error {}".format(status))

    def on_timeout(self):
        print("tweepy timeout.. wait 30 seconds")
        gevent.sleep(30)

stream_listener = MyStreamListener()
stream_listener.start()

def app(environ, start_response):
    ws = environ['wsgi.websocket']
    stream_listener.add_socket(ws)
    while not ws.closed:
        continue

server = pywsgi.WSGIServer(('', 10000), app, handler_class=WebSocketHandler)
server.serve_forever()
