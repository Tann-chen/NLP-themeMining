from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist
from sklearn.metrics import silhouette_score
import numpy as np
from sklearn.decomposition import PCA

from repo import insert

def kmeans(min_clusters, max_clusters, matrix, word_list, corpus_id):
    print("[INFO] doing Kmeans clustering...")
    # reduce vect to 2
    pca = PCA(n_components=2)
    reduce_word_vec = pca.fit_transform(matrix)
    reduce_word_vec_lst = {}
    token_position = {}
    for i in range(0, len(matrix)):
        temp_vec = reduce_word_vec[i]
        temp_vec_lst = list(reduce_word_vec[i])
        temp_token = word_list[i]
        reduce_word_vec_lst[temp_token] = temp_vec
        token_position[temp_token] = temp_vec_lst

    # save token's position to db
    token_position["corpus_id"] = corpus_id
    insert("token_positions", token_position)

    K = range(min_clusters, max_clusters + 1)
    mean_distortions = []
    sc_scores = []
    reduce_word_vec = np.array(reduce_word_vec).reshape(len(reduce_word_vec), 2)

    for k in K:
        kmeans_sk = KMeans(n_clusters=k).fit(reduce_word_vec)
        sc_score = silhouette_score(reduce_word_vec,kmeans_sk.labels_,metric='euclidean')
        mean_distortions.append(sum(np.min(cdist(reduce_word_vec, kmeans_sk.cluster_centers_, 'euclidean'), axis=1)) / reduce_word_vec.shape[0])
        sc_scores.append(sc_score)

    bestK = np.argmax(sc_scores) + min_clusters

    # save infos about every k to db
    docu = {}
    docu["corpus_id"] = corpus_id
    docu["clusters"] = K
    docu["elbow_values"] = mean_distortions
    docu["sc_scores"] = sc_scores
    insert("cluster_analysis", docu)

    # em algo based on best k
    km_2d = KMeans(n_clusters=bestK, algorithm="full").fit(reduce_word_vec)
    y_kmeans = km_2d.predict(reduce_word_vec)

    # get clustered result
    clustered_result = []
    representative_token = []
    for i in range(0, bestK):
        temp = []
        clustered_result.append(temp)

    for i in range(0, len(matrix)):
        cluster_index = (km_2d.labels_)[i]
        clustered_result[cluster_index].append(word_list[i])

    # get representative for every cluster
    for i in range(0, bestK):
        tempValue = 100
        for w in clustered_result[i]:
            distance = calculate_distance(reduce_word_vec_lst.get(w), km_2d.cluster_centers_[i])
            if distance < tempValue:
                tempValue = distance
                representative_token[i] = w

    return_data = {}
    return_data['clusters'] = clustered_result      # clusted list
    return_data['centers'] = km_2d.cluster_centers_     # ceter position
    return_data['representative'] = representative_token   # representative token

    # save theme info for every theme to db
    for i in range(0, bestK):
        docu = {"_id": corpus_id + "#" + str(i)}
        docu["theme"] = representative_token[i]
        docu["tokens"] = clustered_result[i]
        insert("themes", docu)

    return return_data



def calculate_distance(word1, word2):
    distance = np.sqrt(np.sum(np.square(word1 - word2)))
    return distance
