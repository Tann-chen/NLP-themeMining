from flask import Flask, request, jsonify
import datetime
import os
import pickle
from service import service_get_postings_by_token, service_bubble_sort, service_get_ele_by_attr, service_get_theme_by_token
from repo import repo_find_documents, repo_find_document_by_id, repo_find_all, repo_count_documents_within_collection

app = Flask(__name__, static_url_path='/static')

@app.route('/api/init',methods=['GET'])
def init_page():
    result = {}
    # get pie chart data
    pie_data = []

    lst_theme = list(repo_find_all("themes"))

    for one_theme_doc in lst_theme:
        accumulator = 0
        theme = one_theme_doc["themes"]
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
    for d in pie_data:
        if max_count < d.get("count"):
            max_count = d.get("count")
            max_theme = d.get("item")

    lst_tokens = []
    for one_theme_doc in lst_theme:
        if one_theme_doc["themes"] == max_theme:
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
    result["bar_chart_data"] = bar_data
    result["largest_theme"] = max_theme

    return jsonify(result)


@app.route('/api/data/bar_chart',methods=['GET'])
def get_bar_chart_data():
    selected_theme = request.args.get('theme')
    bar_data = []
    # get from database about every theme cover what words
    dict_criteria = {}
    dict_criteria["themes"] = selected_theme
    docu = list(repo_find_documents("themes", dict_criteria))[0]
    lst_tokens = docu["tokens"]
    for t in lst_tokens:
        postings = service_get_postings_by_token(t, en_inversed_index, fr_inversed_index)
        entry = {}
        entry["token"] = t
        entry["count"] = len(postings)
        bar_data.append(entry)

    # sort bar data based on "count"
    service_bubble_sort(bar_data, "count")

    return jsonify(bar_data)


@app.route('/api/data/line_char',methods=['GET'])
def get_line_chart_data():
    line_data = []
    # get from database
    K_analysis = list(repo_find_all("cluster_analysis"))

    for k_doc in K_analysis:
        entry = {}
        entry["num_cluster"] = k_doc['K']
        entry["elobow"] = k_doc['elbow_val']
        entry["SC_score"] = k_doc['sc_score']
        line_data.append(entry)

    return jsonify(line_data)


@app.route('/api/data/point_chart',methods=['GET'])
def get_point_chart_data():
    point_data = []
    # get from database about positions
    dict_token_positions = list(repo_find_all("token_locations"))[0]
    # get from database about theme
    lst_theme_doc = list(repo_find_all("themes"))

    dict_theme_tokens = {}
    for theme_doc in lst_theme_doc:
        dict_theme_tokens[theme_doc["themes"]] = theme_doc["tokens"]

    #dict_token_positions['_id'] = 0

    for token, lst_position in dict_token_positions.items():
        if token.startswith('_'):
            continue

        x = lst_position[0]
        y = lst_position[1]
        entry = {}
        theme = service_get_theme_by_token(token, dict_theme_tokens)
        entry["theme"] = theme
        entry["token"] = token
        entry["x"] = x
        entry["y"] = y
        point_data.append(entry)

    return jsonify(point_data)


@app.route('/api/data/sentence',methods=['GET'])
def get_related_sentence():
    sentence_data = []
    selected_theme = request.args.get('theme')

    dict_criteria = {}
    dict_criteria["themes"] = selected_theme
    docu = list(repo_find_documents("themes", dict_criteria))[0]
    lst_tokens = docu["tokens"]

    all_postings = []
    for t in lst_tokens:
        temp_postings = service_get_postings_by_token(t, en_inversed_index, fr_inversed_index)
        for sentence_id in temp_postings:
            all_postings.append(sentence_id)

    # remove duplicated
    all_postings = set(all_postings)
    for i in all_postings:
        doc = repo_find_document_by_id("corpus", i, True)
        txt = doc["content"]
        sentence_data.append(txt)

    return jsonify(sentence_data)


@app.route('/api/data/grid_chart',methods=['GET'])
def get_grid_chart_data():
    grid_data = {}

    # get from database
    # now only first is avail
    query_similarity = list(repo_find_all("queries"))[0]

    grid_data["question"] = query_similarity["question"]
    grid_data["query_tokens"] = query_similarity["query_tokens"]
    grid_data["themes"] = query_similarity["themes"]
    grid_data["similarity"] = query_similarity["similarity"]

    return jsonify(grid_data)


if __name__ == '__main__':
    # load inverse index from file to memory
    with open('../model/out/index_en.pickle', 'rb') as file:
        en_inversed_index = pickle.load(file)

    with open('../model/out/index_fr.pickle', 'rb') as file:
        fr_inversed_index = pickle.load(file)

    # precompute global data
    total_token_freq = 0
    for postings in list(en_inversed_index.values()):
        total_token_freq = total_token_freq + len(postings)
    for postings in list(fr_inversed_index.values()):
        total_token_freq = total_token_freq + len(postings)

    # app run
    app.run()
