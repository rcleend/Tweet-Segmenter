class Comparer:
    def filter_segments(self, my_segments, twitter_segments):
        # Remove all segments from twitter_segments that exist in my_segments
        return [x for x in twitter_segments if x not in my_segments]
