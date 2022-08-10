import json

"""
TODO: Prototype 1

1.1 return values from test.json
"""


class TwitterAPI:
    def get_tweets(self):
        response = open('utils/twitter_api/test.json', 'r')
        tweets = json.load(response)
        response.close()

        return tweets

