from utils.twitter_api.main import TwitterAPI
from utils.cleaner import TweetCleaner
from utils.segmenter import SEDTWikSegmenter
from utils.clusterer import Clusterer
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
tweet_segmenter = SEDTWikSegmenter(wiki_titles_file='data/enwiki-titles-unstemmed.txt')

tweets = twitter_api.get_tweets()
cleaned_tweets = tweet_cleaner.clean_tweets(tweets)

for tweet in cleaned_tweets['data']:
    print(tweet_segmenter.tweet_segmentation(tweet))

# TODO: cluster segmentations
clusterer = Clusterer()






