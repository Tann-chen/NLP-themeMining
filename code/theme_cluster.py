from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist
from sklearn.metrics import silhouette_score
import numpy as np
from sklearn.decomposition import PCA
from repo import insert


IF_DEBUG = True

def kmeans(max_clusters, matrix, word_list):
    if IF_DEBUG:
        print("[INFO] start doing Kmeans clustering...")
    # reduce vect to 2
    pca = PCA(n_components=2)
    reduce_word_vec = pca.fit_transform(matrix)
    reduce_word_vec_lst = {}

    for i in range(0, len(matrix)):
        temp_vec = reduce_word_vec[i]
        temp_token = word_list[i]
        reduce_word_vec_lst[temp_token] = temp_vec

    K = range(3, max_clusters)
    mean_distortions = []
    sc_scores = []

    reduce_word_vec = np.array(reduce_word_vec).reshape(len(reduce_word_vec),2)

    for k in K:
        kmeans_sk = KMeans(n_clusters=k).fit(reduce_word_vec)
        sc_score = silhouette_score(reduce_word_vec,kmeans_sk.labels_,metric='euclidean')
        mean_distortions.append(sum(np.min(cdist(reduce_word_vec, kmeans_sk.cluster_centers_, 'euclidean'), axis=1)) / reduce_word_vec.shape[0])
        sc_scores.append(sc_score)

    bestK = np.argmax(sc_scores) + 3

    # repo
    for i in K:
        input_cluster_analysis = {"K":i}
        input_cluster_analysis["elbow_val"] = mean_distortions[i - 3]
        input_cluster_analysis["sc_score"] = sc_scores[i - 3]
        insert("cluster_analysis", input_cluster_analysis)

    # em algo based on best k
    km_2d = KMeans(n_clusters= bestK, algorithm="full").fit(reduce_word_vec)
    y_kmeans = km_2d.predict(reduce_word_vec)

    # get representative token for every theme
    clustered_result = []
    representative_token = []
    for i in range(0, bestK):
        temp = []
        clustered_result.append(temp)
        representative_token.append(temp)

    for i in range(0, len(matrix)):
        index_word = (km_2d.labels_)[i]
        clustered_result[index_word].append(word_list[i])

    for i in range(0, bestK):
        tempValue = 100
        for w in clustered_result[i]:
            distance = calculate_distance(reduce_word_vec_lst.get(w), km_2d.cluster_centers_[i])
            if distance < tempValue:
                tempValue = distance
                representative_token[i] = w

    return_data = {}
    return_data['clusters'] = clustered_result
    return_data['centers'] = km_2d.cluster_centers_
    return_data['representative'] = representative_token

    # repo tokens_list for every theme
    for i in range(0, bestK):
        input_theme = {"_id": "theme" + str(i)}
        input_theme["themes"] = representative_token[i]
        input_theme["tokens"] = clustered_result[i]
        insert("themes",input_theme)

    return return_data



def calculate_distance(word1, word2):
    distance = np.sqrt(np.sum(np.square(word1 - word2)))
    return distance
