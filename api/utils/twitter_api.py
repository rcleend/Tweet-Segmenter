import requests
import json
import os
from dotenv import load_dotenv


class TwitterAPI:
    def __init__(self):
        load_dotenv()
        self.__search_url = "https://api.twitter.com/2/tweets/search/recent"
        self.__bearer_token = os.environ.get("BEARER_TOKEN")

    def __bearer_oauth(self, r):
        r.headers["Authorization"] = f"Bearer {self.__bearer_token}"
        r.headers["User-Agent"] = "v2RecentSearchPython"
        return r

    def get_tweets(self, query, max_results=100, amount_of_requests=1):
        print('Getting response from Twitter api...')
        params = {'query': query + ' lang:en', 'max_results': max_results}
        response_dict = {'data': [], 'meta': {}}

        for i in range(0, amount_of_requests):
            if(i > 0):
                params['next_token'] = response_dict['meta']['next_token']

            response = requests.get(self.__search_url, auth=self.__bearer_oauth, params=params)
            if response.status_code != 200:
                raise Exception(response.status_code, response.text)

            json_data = json.loads(response.text)
            response_dict['data'].extend(json_data['data'])
            response_dict['meta'] = json_data['meta']

        return response_dict

        # response = open('response.json', 'r')
        # tweets = json.load(response)
        # response.close()

        # return tweets

