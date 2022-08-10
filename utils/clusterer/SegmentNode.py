class SegmentNode:
    def __init__(self, segment, prev):
        self.segment = segment
        self.prev = prev
        self.count = 1

    def update(self):
        # TODO: check if update is correct
        self.count += 1
        prev = self.prev
        self.prev = prev.prev
        prev.prev = self


