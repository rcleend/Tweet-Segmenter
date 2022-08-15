from twitter_api.main import TwitterAPI
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

clusterer = Clusterer()

for tweet in cleaned_tweets['data']:
    clusterer.add_segments(tweet_segmenter.tweet_segmentation(tweet))

clusterer.create_clusters()
clusterer.save_clusters_to_json()






