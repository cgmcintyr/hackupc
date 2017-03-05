# -*- coding: utf-8 -*-
"""Everything sentiment analysis"""

from __future__ import print_function
import requests
import json
import requests
import random

supported_langs = {'en':'English', 'es':'Spanish'}

headers = {
    'x-api-key': '9CAfxmC4WB10tnS9RY9oG92Io0M4trVp7HpTUEjR',
    'Content-Type': 'application/json',
}

def get_language(text_in):
    data = {"textIn": text_in}
    r = requests.post('https://jmlk74oovf.execute-api.eu-west-1.amazonaws.com/dev/language?wait=true', headers=headers, data=json.dumps(data))
    content = r.json()
    return content['results']['language']

def get_sentiment(text_in, language='English'):
    data = {"textIn": text_in,  "language": language}
    r = requests.post('https://jmlk74oovf.execute-api.eu-west-1.amazonaws.com/dev/sentiment?wait=true', headers=headers, data=json.dumps(data))
    content = r.json()
    prediction = content['results']['prediction']

    if prediction == 'neutral' and random.random() > 0.33:
        prediction = 'positive'
    else:
        prediction = 'negative'

    return prediction
