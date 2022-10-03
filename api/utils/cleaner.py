# See the original pyTweetCleaner at https://github.com/kevalmorabia97/pyTweetCleaner

import re
import string

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


class Cleaner:
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
        for tweet in tweets['data']:
            tweet['text'] = self.get_cleaned_text(tweet['text'])

        return tweets
