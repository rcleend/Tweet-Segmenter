# See the original pyTweetCleaner at https://github.com/kevalmorabia97/pyTweetCleaner

"""
REMOVE:        TWEETS THAT HAVE in_reply_to_status_id !=null i.e. COMMENTS ON SOMEONE ELSE'S TWEETS
               TWEETS THAT HAVE lang != en i.e. NOT IN ENGLISH LANGUAGE
               DATA ABOUT DELETED TWEETS
               NON-ASCII CHARACTERS FROM text
               HYPERLINKS FROM text
               STOPWORDS from text
               #tags & @name mentions
               digits[0-9] FROM text

KEEP:          created_at
               id
               text IN LOWERCASE
               user_id
               user_followers_count
               retweet_count
               entities_hashtags, entities_user_mentions
               retweeted_status REPLACES ACTUAL tweet BUT PRESERVES RETWEETER'S USER INFO
"""

import json
import re
import string

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


class TweetCleaner:
    def __init__(self, remove_stop_words=False, remove_retweets=False):
        """
        clean unnecessary twitter data
        """
        if remove_stop_words:
            self.stop_words = set(stopwords.words('english'))
        else:
            self.stop_words = set()

        self.remove_retweets = remove_retweets

        self.punc_table = str.maketrans("", "", string.punctuation)  # to remove punctuation from each word in tokenize

    def remove_non_ascii_chars(self, text):
        """
        return text after removing non-ascii characters i.e. characters with ascii value >= 128
        """
        return ''.join([w if ord(w) < 128 else ' ' for w in text])

    def remove_hyperlinks(self, text):
        """
        return text after removing hyperlinks
        """
        return ' '.join([w for w in text.split(' ') if not 'http' in w])

    def get_cleaned_text(self, text):
        cleaned_text = text.replace('\"', '').replace('\'', '').replace('-', ' ')
        cleaned_text = self.remove_non_ascii_chars(cleaned_text)
        cleaned_text = self.remove_hyperlinks(cleaned_text)

        # remove digits
        cleaned_text = re.sub('[0-9]+', '', cleaned_text)

        # remove hashtags
        cleaned_text = re.sub('#[_a-zA-Z][_a-zA-Z0-9]*', '', cleaned_text)

        # remove @name
        cleaned_text = ' '.join([w for w in cleaned_text.split() if not w.startswith('@')])

        tokens = [w.translate(self.punc_table) for w in word_tokenize(cleaned_text)]  # remove punctuations and tokenize
        tokens = [w.lower() for w in tokens if not w.lower() in self.stop_words and len(w) > 1]
        cleaned_text = ' '.join(tokens)

        return cleaned_text

    def clean_tweets(self, tweets):
        """
        tweets: json formatted response of twitter API tweets
        output_file: file name or path where cleaned twitter json data is stored (default='cleaned_tweets.json')
        """
        for tweet in tweets['data']:
            tweet['text'] = self.get_cleaned_text(tweet['text'])

        return tweets


if __name__ == '__main__':
    tc = TweetCleaner(remove_stop_words=True, remove_retweets=True)
    print(tc.get_cleaned_text(
        'The movie The Twilight Saga: New Moon was the biggest winner in MTV Movie Awards 2010; it took 4 out of 10 "Best" Awards #IAmGreat'))

    print('\nTweetCleaning DONE...')
