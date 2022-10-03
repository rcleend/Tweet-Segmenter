from utils.twitter_api import TwitterAPI
from utils.cleaner import TweetCleaner
from utils.segmenter import SEDTWikSegmenter
import json

"""
TODO: Prototype 1

1.1 Get test tweets
1.2 Clean Tweets
1.3 Segment Tweets
1.3 Store Tweet Segments

2.1 Get input from document
2.2 Clean Document
2.2 Segment Document

3.1 Compare Segmented Document to Stored Tweet Segments
"""

twitter_api = TwitterAPI()
tweet_cleaner = TweetCleaner()
tweet_segmenter = SEDTWikSegmenter(wiki_titles_file='data/enwiki-titles-unstemmed-no-stopwords-all.txt')

tweets = twitter_api.get_tweets('(Ukraine OR Russia) -is:retweet', 100, 2)

# with open("response.json", "w") as write_file:
#     json.dump(tweets, write_file, indent=4)

cleaned_tweets = tweet_cleaner.clean_tweets(tweets)

# with open("cleaned_tweets.json", "w") as write_file:
#     json.dump(cleaned_tweets, write_file, indent=4)


for tweet in cleaned_tweets['data']:
    print(tweet)
    print(tweet_segmenter.tweet_segmentation(tweet))

# with open("segmentations.json", "w") as write_file:
#     json.dump(cleaned_tweets, write_file, indent=4)

