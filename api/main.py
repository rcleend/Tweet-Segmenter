from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models.twitter_request import TwitterRequest
from models.twitter_response import TwitterResponse

from utils.twitter_api import TwitterAPI
from utils.cleaner import Cleaner
from utils.segmenter import SEDTWikSegmenter
from utils.grouper import Grouper
from utils.comparer import Comparer


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # TODO: fix wildcard
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

twitter_api = TwitterAPI()
cleaner = Cleaner(True, True)
segmenter = SEDTWikSegmenter(wiki_titles_file='../data/enwiki-titles-unstemmed-no-stopwords-all.txt')
grouper = Grouper()
comparer = Comparer()


@app.post("/twitter", response_model=TwitterResponse)
async def query(body: TwitterRequest):
    # Get relevant Tweets
    tweets = twitter_api.get_tweets(body.query, 100, body.amount_multiplier)

    # Clean tweets and article
    tweets_cleaned = cleaner.clean_tweets(tweets)
    text_cleaned = cleaner.get_cleaned_text(body.selected_text)

    # Create Segments
    tweet_segments = []
    [tweet_segments.extend(segmenter.tweet_segmentation(tweet)) for tweet in tweets_cleaned['data']]
    text_segments = segmenter.text_segmentation(text_cleaned)

    # Compare text and tweet segments
    unique_segments = comparer.filter_segments(text_segments, tweet_segments)

    # Group by stemmed segment and sort by frequency
    grouped_results = grouper.group_by_stem_and_sort_by_freq(unique_segments)

    # Create JSON response
    json_results = []
    for result in grouped_results:
        json_results.append({
            "segment": result[0].title(),
            "frequency": result[2]
        })

    return {
        "original_query": body.query,
        "results": json_results
    }
