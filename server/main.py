from flask import Flask, request, jsonify
import datetime
import os
import math
import pickle
from service import service_get_postings_by_token, service_bubble_sort, service_get_theme_by_token
from repo import repo_find_documents, repo_find_document_by_id, repo_find_all, repo_count_documents_within_collection

app = Flask(__name__, static_url_path='/static')

@app.route('/api/corpus', methods=['GET'])
def get_corpus_infos():
    corpus_infos = []
    lst_corpus = list(repo_find_all('corpus'))
    for one_corpus_doc in lst_corpus:
        entry = {}
        entry["corpus_id"] = one_corpus_doc["create_time"].replace('-','').replace(':','')
        entry["corpus_description"] = one_corpus_doc["description"]
        entry["create_time"] = one_corpus_doc["create_time"]
        entry["samples_size"] = one_corpus_doc["samples_size"]
        entry["samples_num"] = one_corpus_doc["samples_num"]
        entry["sentences_num"] = one_corpus_doc["sentences_num"]
        entry["tokens_num"] = one_corpus_doc["tokens_num"]
        entry["queries_num"] = one_corpus_doc["queries_num"]
        entry["themes_num"] = one_corpus_doc["themes_num"]
        corpus_infos.append(entry)

    return jsonify(corpus_infos)


@app.route('/api/corpus/query', methods=['GET'])
def get_corpus_queries():
    selected_corpus_id = request.args.get('corpus')
    query_infos = []
    criteria = {"corpus_id", selected_corpus_id}
    lst_query = list(repo_find_documents('queries', criteria));
    for one_query in lst_query:
        entry = {}
        entry["query_id"] = one_query["_id"]
        entry["question"] = one_query["question"]
        query_infos.append(entry)

    return jsonify(query_infos)


@app.route('/api/analysis', methods=['GET'])
def get_analysis_data():
    selected_corpus_id = request.args.get('corpus')
    result = {}
    # get pie chart data
    pie_data = []

    # loading indexing
    path = '../model/out/'
    with open(path + selected_corpus_id + '_en.pickle', 'rb') as file:
        en_inversed_index = pickle.load(file)
    with open(path + selected_corpus_id + '_fr.pickle', 'rb') as file:
        fr_inversed_index = pickle.load(file)

    # read from db
    criteria = {"corpus_id", selected_corpus_id}
    lst_theme = list(repo_find_documents("themes", criteria))

    for one_theme_doc in lst_theme:
        accumulator = 0
        theme = one_theme_doc["theme"]
        lst_tokens = one_theme_doc["tokens"]
        for t in lst_tokens:
            temp_postings = service_get_postings_by_token(t, en_inversed_index, fr_inversed_index)
            accumulator = accumulator + len(temp_postings)
        # pack result in dict
        entry = {}
        entry["item"] = theme
        entry["count"] = accumulator
        pie_data.append(entry)

    result["pie_chart_data"] = pie_data

    # get bar chart data matching largest pie
    bar_data = []
    max_theme = ''
    max_count = 0
    for d in pie_data:      # get theme with max token_num
        if max_count < d.get("count"):
            max_count = d.get("count")
            max_theme = d.get("item")

    lst_tokens = []
    for one_theme_doc in lst_theme:     # get token list of max_theme
        if one_theme_doc["theme"] == max_theme:
            lst_tokens = one_theme_doc["tokens"]
            break

    for t in lst_tokens:
        postings = service_get_postings_by_token(t, en_inversed_index, fr_inversed_index)
        entry = {}
        entry["token"] = t
        entry["count"] = len(postings)
        bar_data.append(entry)

    # sort bar data based on "count"
    service_bubble_sort(bar_data, "count")
    result["largest_theme"] = max_theme
    result["bar_chart_data"] = bar_data

    # release index
    del en_inversed_index
    del fr_inversed_index

    return jsonify(result)


@app.route('/api/data/bar_chart', methods=['GET'])
def get_bar_chart_data():
    selected_corpus_id = request.args.get('corpus')
    selected_theme = request.args.get('theme')

    # loading indexing
    path = '../model/out/'
    with open(path + selected_corpus_id + '_en.pickle', 'rb') as file:
        en_inversed_index = pickle.load(file)
    with open(path + selected_corpus_id + '_fr.pickle', 'rb') as file:
        fr_inversed_index = pickle.load(file)

    bar_data = []
    # get from database about every theme cover what words
    criteria = {"theme": selected_theme, "corpus_id": selected_corpus_id}
    docu = list(repo_find_documents("themes", criteria))[0]
    lst_tokens = docu["tokens"]
    for t in lst_tokens:
        postings = service_get_postings_by_token(t, en_inversed_index, fr_inversed_index)
        entry = {}
        entry["token"] = t
        entry["count"] = len(postings)
        bar_data.append(entry)

    # sort bar data based on "count"
    service_bubble_sort(bar_data, "count")

    del en_inversed_index
    del fr_inversed_index

    return jsonify(bar_data)


@app.route('/api/data/line_char', methods=['GET'])
def get_line_chart_data():
    selected_corpus_id = request.args.get('corpus')

    line_data = []
    # get from database
    criteria = {"corpus_id": selected_corpus_id}
    docu = list(repo_find_documents("cluster_analysis", criteria))
    lst_cluster = docu["clusters"]
    lst_elbow_val = docu["elbow_values"]
    lst_sc_scores = docu["sc_scores"]

    for i in range(0, len(lst_cluster)):
        entry = {}
        entry["num_cluster"] = lst_cluster[i]
        entry["elobow"] = lst_elbow_val[i]
        entry["SC_score"] = lst_sc_scores[i]
        line_data.append(entry)

    return jsonify(line_data)


@app.route('/api/data/point_chart', methods=['GET'])
def get_point_chart_data():
    selected_corpus_id = request.args.get('corpus')

    point_data = []
    # get from database about positions
    criteria = {"corpus_id": selected_corpus_id}
    positions_docu = list(repo_find_documents("token_positions", criteria))[0]
    lst_theme = list(repo_find_documents("themes", criteria))

    dict_theme_tokens = {}
    for theme_doc in lst_theme:
        dict_theme_tokens[theme_doc["theme"]] = theme_doc["tokens"]

    for token, position in positions_docu.items():
        if token.startswith("_") or token == "corpus_id" :
            continue

        x = position[0]
        y = position[1]
        theme = service_get_theme_by_token(token, dict_theme_tokens)
        entry = {}
        entry["theme"] = theme
        entry["token"] = token
        entry["x"] = x
        entry["y"] = y
        point_data.append(entry)

    return jsonify(point_data)


@app.route('/api/data/sentence', methods=['GET'])
def get_related_sentence():
    selected_corpus_id = request.args.get('corpus')
    selected_token = request.args.get('token')

    sentence_data = []

    # loading indexing
    path = '../model/out/'
    with open(path + selected_corpus_id + '_en.pickle', 'rb') as file:
        en_inversed_index = pickle.load(file)
    with open(path + selected_corpus_id + '_fr.pickle', 'rb') as file:
        fr_inversed_index = pickle.load(file)

    postings = service_get_postings_by_token(selected_token, en_inversed_index, fr_inversed_index)
    # remove duplicated & sort
    postings = list(set(postings)).sort()

    # algorithem to reduce access of db
    for index in range(0, len(postings)):
        curr_min_id = postings[index]
        doc_id = math.floor(curr_min_id / CORPUS_DOC_STEP)
        corpus_doc_id = selected_corpus_id + '#' + doc_id
        docu = repo_find_document_by_id("corpus", corpus_doc_id)
        max_doc_index = docu["max_index"]
        dict_sentences = docu["content"]
        while postings[index] <= max_doc_index:
            txt = dict_sentences.get(postings[index])   # index: sentence
            sentence_data.append(txt)
            index = index + 1

    del en_inversed_index
    del fr_inversed_index

    return jsonify(sentence_data)


@app.route('/api/data/grid_chart',methods=['GET'])
def get_grid_chart_data():
    selected_query_id = request.args.get('query')

    grid_data = {}
    docu = list(repo_find_document_by_id("queries", selected_query_id))[0]
    grid_data["question"] = docu["question"]
    grid_data["query_tokens"] = docu["query_tokens"]
    grid_data["themes"] = docu["themes"]
    grid_data["similarity"] = docu["similarity"]
    return jsonify(grid_data)


if __name__ == '__main__':
    CORPUS_DOC_STEP = 20
    app.run()
