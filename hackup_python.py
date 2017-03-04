from __future__ import print_function
import requests
import json
import requests

# tweets = list of tweets to analyze, we need to specify the language as well
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
