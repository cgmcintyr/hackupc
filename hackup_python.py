'''
Title           :hackup_python.py
Description     :This is a sample code for calling two everisMoriarty 
				services that do language detection and sentiment analysis.
				These services were specifically prepared for HackUPC 2017
				event, and will stop running on 05/03/2017 at 11pm.
Author          :Adil Moujahid <mohammed.adil.sa@everis.com>
Date Created    :20170224
Date Modified   :20170301
version         :0.4
usage           :python make_predictions_2.py
python_version  :2.7.11
'''

from __future__ import print_function
import requests
import json
import requests

tweets = [["Estoy genial!","Spanish"],["This is a big shit","English"]]

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
    return content['results']['prediction']

for i in range(2):
	print(get_sentiment(tweets[i][0],tweets[i][1]))
