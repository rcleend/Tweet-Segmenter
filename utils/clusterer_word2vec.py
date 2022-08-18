from gensim.models import KeyedVectors
from sklearn.decomposition import PCA
import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import numpy as np


class ClustererWord2Vec:
    def __init__(self):
        # load into word2vec

        print('Loading keyed vectors')
        self.__keyed_vectors = KeyedVectors.load_word2vec_format('../data/enwiki_keyed_vectors.txt')
        # print('Finished loading keyed vectors')
        #
        # print('Loading all titles')
        # wiki_titles = []
        # f = open('../data/enwiki_titles.txt', 'r')
        # for title in f:
        #     wiki_titles.append(title)
        #
        # print(wiki_titles)
        #
        # print('Finished loading all titles')

    def fit_model(self, n_components=2):
        vectors = self.__keyed_vectors[self.__wiki_titles]
        pca = PCA(n_components=n_components)
        words = pd.DataFrame(self.__wiki_titles)
        pca_result = pd.DataFrame(pca.fit_transform(vectors))
        pca_result['x_values'] = pca_result.iloc[0:, 0]
        pca_result['y_values'] = pca_result.iloc[0:, 1]
        print(pca_result[['x_values', 'y_values']])

        pca_final = pd.merge(words, pca_result, left_index=True, right_index=True)
        pca_final['word'] = pca_final.iloc[0:, 0]

        pca_data_complete = pca_final[['word', 'x_values', 'y_values']]
        print(pca_data_complete)

        # create x = [x_values, y_values]
        X = StandardScaler().fit_transform(pca_result[['x_values', 'y_values']])

        db = DBSCAN(eps=0.3, min_samples=10).fit(X)
        core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
        core_samples_mask[db.core_sample_indices_] = True
        labels = db.labels_

        # Number of clusters in labels, ignoring noise if present.
        n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
        n_noise_ = list(labels).count(-1)

        print("Estimated number of clusters: %d" % n_clusters_)
        print("Estimated number of noise points: %d" % n_noise_)

if __name__ == '__main__':
    clusterer = ClustererWord2Vec()
    # clusterer.fit_model()



