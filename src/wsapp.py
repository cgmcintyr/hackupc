import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
from datetime import timedelta
import json
import tweepy
from tweepy import OAuthHandler
import threading
from collections import namedtuple

from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException

# Authentication params
# Refer to https://dev.twitter.com/oauth/overview/application-owner-access-tokens
from config import *
from cities import bounding
from sentiment import get_sentiment, supported_langs

Tweet = namedtuple('Tweet', ['id', 'place', 'user', 'text', 'sentiment'])


class WSHandler(tornado.websocket.WebSocketHandler):
    connections = []
    
    def check_origin(self, origin):
        return True

    def open(self):
        print 'Connection established.'
        self.connections.append(self)
    
    # When message arrives write it to websocket
    def on_message(self, message):
        print 'Tweet received: \"%s\"' % message
        self.write_message(message)
           
    def on_close(self):
        print 'Conn closed...'
        self.connections.remove(self)


class MyStreamListener(tweepy.StreamListener, WSHandler):
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
            s = get_sentiment(text, supported_langs[lang])
            tweet = Tweet(tweetid, place, user, text, s)
            print(tweet)
            for connection in WSHandler.connections:
                data = json.dumps(tweet.__dict__).encode('utf-8')
                connection.write_message(data)
        else:
            print("detected lang '{}' is not supported".format(lang))

        return True

    # limit handling
    def on_limit(self, status):
        print 'Limit threshold exceeded', status
    
    def on_timeout(self, status):
        print 'Stream disconnected; continuing...'  

    # error handling
    def on_error(self, status_code):
        if status_code == 420:
            return False


def OpenStream():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    stream = tweepy.Stream(auth, MyStreamListener()) 
    stream.filter(locations=bounding['spain'])


if __name__ == "__main__":
    threading.Thread(target=OpenStream).start()
    application = tornado.web.Application([
        (r'/ws', WSHandler),
        (r'/(favicon.ico)', tornado.web.StaticFileHandler, {'path': 'favicon.ico'}) # path to your icon
    ])
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
