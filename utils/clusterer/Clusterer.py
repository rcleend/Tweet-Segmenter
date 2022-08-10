from SegmentNode import SegmentNode

class Clusterer:
    def __init__(self, segments):
        self.segment_dictionary = {}

        for segment in segments:
            if segment not in self.segment_dictionary:
                node = SegmentNode(segment, self.last_added_item)
                self.segment_dictionary[segment] = node
                self.last_added_item = node
            else:
                self.segment_dictionary[segment].update()

    def get_most_frequenty(self, min_frequency):
        # TODO: implement
        print(min_frequency)
