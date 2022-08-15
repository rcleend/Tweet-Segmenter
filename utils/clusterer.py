import numpy as np
from sklearn.cluster import AffinityPropagation
import distance
import json

class Clusterer:
    def __init__(self):
        self.segments = []
        self.__affprop = AffinityPropagation(affinity="precomputed", damping=0.5)

    def add_segments(self, segments):
        self.segments += segments

    def __get_level_similarity(self):
        self.segments = np.asarray(self.segments)  # So that indexing with a list will work
        return -1 * np.array([[distance.levenshtein(w1, w2) for w1 in self.segments] for w2 in self.segments])

    def create_clusters(self):
        test = self.__get_level_similarity()
        self.__affprop.fit(test)

    def save_clusters_to_json(self):
        clusters_dict = {}
        for cluster_id in np.unique(self.__affprop.labels_):
            exemplar = self.segments[self.__affprop.cluster_centers_indices_[cluster_id]]
            cluster = np.unique(self.segments[np.nonzero(self.__affprop.labels_ == cluster_id)])
            clusters_dict[exemplar] = cluster.tolist()

        with open("test.json", "w") as write_file:
            json.dump(clusters_dict, write_file, indent=4)