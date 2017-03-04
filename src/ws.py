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
from tweepy import Stream
import json

import tweepy
from langdetect import detect
from collections import namedtuple

from cities import cities
from config import *
from sentiment import get_sentiment, supported_langs

Tweet = namedtuple('Tweet', ['city', 'latitdue', 'longitude', 'sentiment', 'text'])

class MyStreamListener(StreamListener):
    def __init__(self, cities, limit):
        self.status_count = 0
        self.status_stop_count = limit
        self.cities = cities

        self.sockets = []
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_key, access_secret)
        self.api = tweepy.API(auth)
        self.stream = Stream(auth, self)

    def switch_city(self):
        self.city = random.choice(self.cities)
        self.latitude = self.city.latitude
        self.longitude = self.city.longitude

    def add_socket(self, ws):
        self.sockets.append(ws)

    def run(self):
        try:
            self.switch_city()
            self.stream.filter(locations=self.city.bounding)
        except Exception:
            print(traceback.format_exc())
            print(sys.exc_info()[0])
            self.stream.disconnect()

    def start(self):
        gevent.spawn(self.run)

    def send(self, ws, data):
        try:
            ws.send(data)
        except Exception:
            # the web socket die..
            self.sockets.remove(ws)

    def on_status(self, status):
        print("on_status")
        lang = None

        try:
            lang = detect(status.text)
        except LangDetectException:
            pass

        if lang in supported_langs.keys():
            self.status_count += 1
            s = get_sentiment(status.text, supported_langs[lang])
            h = Tweet(self.city, self.latitude, self.longitude, s, status.text)
            for ws in self.sockets:
                gevent.spawn(self.send, ws, json.dumps(h.__dict__))

        if self.status_count == self.status_stop_count:
            self.status_count = 0
            self.stream.disconnect()
            self.run()

    def on_error(self, status):
        print("Error {}".format(status))

    def on_timeout(self):
        print("tweepy timeout.. wait 30 seconds")
        gevent.sleep(30)

stream_listener = MyStreamListener(cities, 3)
stream_listener.start()

def app(environ, start_response):
    ws = environ['wsgi.websocket'.encode('utf-8')]
    stream_listener.add_socket(ws)
    while not ws.closed:
        gevent.sleep(0.1)

server = pywsgi.WSGIServer(('', 10000), app, handler_class=WebSocketHandler)
server.serve_forever()
