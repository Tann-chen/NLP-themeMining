from flask import Flask, request, jsonify
import datetime
import os
import pickle
import service
import repo

app = Flask(__name__, static_url_path='../front')

@app.route('/api/init',methods=['GET'])
def init_page():
    result = {}
    # get pie chart data
    pie_data = []

    lst_theme = list(repo.find_all("themes"))

    for one_theme_doc in lst_theme:
        accumulator = 0
        theme = one_theme_doc["theme"]
        lst_tokens = one_theme_doc["tokens"]
        for t in lst_tokens:
            temp_postings = service.get_postings_by_token(t, en_inversed_index, fr_inversed_index)
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

    lst_tokens = lst_theme.get(max_theme)
    for t in lst_tokens:
        postings = service.get_postings_by_token(t, en_inversed_index, fr_inversed_index)
        entry = {}
        entry["token"] = t
        entry["count"] = len(postings)
        bar_data.append(entry)

    # sort bar data based on "count"
    service.bubble_sort(bar_data, "count")
    result["bar_chart_data"] = bar_data

    return jsonify(result)


@app.route('/api/data/bar_chart',methods=['GET'])
def get_bar_chart_data():
    selected_theme = request.args.get('theme')
    bar_data = []
    # get from database about every theme cover what words
    dict_criteria = {"theme", selected_theme}
    docu = list(repo.find_documents("themes", dict_criteria))[0]
    lst_tokens = docu["tokens"]
    for t in lst_tokens:
        postings = service.get_postings_by_token(t, en_inversed_index, fr_inversed_index)
        entry = {}
        entry["token"] = t
        entry["count"] = len(postings)
        bar_data.append(entry)

    # sort bar data based on "count"   
    service.bubble_sort(bar_data, "count")

    return jsonify(bar_data)


@app.route('/api/data/line_char',methods=['GET'])
def get_line_chart_data():
    line_data = []
    # get from database
    elobow_valus = []
    SC_scores = []

    for num_cluster, elobow_val in elobow_valus:
        sc_score = service.get_ele_by_attr(SC_scores, "num_cluster", num_cluster)
        entry = {}
        entry["num_cluster"] = num_cluster
        entry["elobow"] = elobow_val
        entry["SC_score"] = sc_score
        line_data.append(entry)

    return jsonify(line_data)


@app.route('/api/data/point_chart',methods=['GET'])
def get_point_chart_data():
    point_data = []
    # get from database about every theme cover what words
    dict_token_positions = {}
    # get from database about every theme cover what words
    lst_theme = {}

    for token, lst_position in dict_token_positions:
        x = lst_position[0]
        y = lst_position[1]
        entry = {}
        theme = service.get_theme_by_token(token)
        entry["theme"] = theme
        entry["token"] = token
        entry["x"] = x
        entry["y"] = y
        point_data.append(entry)

    return jsonify(point_data)


@app.route('/api/data/sentence',methods=['GET'])
def get_related_sentence():
    selected_theme = request.args.get('theme')
    seleted_page = request.args.get('page')

    # get from database about every theme cover what words
    dict_theme = {}







@app.route('/api/data/grid_chart',methods=['GET'])
def get_grid_chart_data():
    grid_data = {}
    # get from database about every theme cover what words
    dict_theme = {}
    df_query = ""
    query_tokens = list(set(service.tokenize_query(df_query)))
    lst_theme = list(dict_theme.keys())
    grid_data["themes"] = lst_theme
    grid_data["query_tokens"] = query_tokens
    grid_data["similarity"] = grid_data
    # calculate similarity
    return


if __name__ == '__main__':
    # load inverse index from file to memory
    with open('en_index.pickle', 'rb') as file:
        en_inversed_index = pickle.load(file)

    with open('fr_index.pickle', 'rb') as file:
        fr_inversed_index = pickle.load(file)

    # precompute global data
    total_token_freq = 0
    for postings in list(en_inversed_index.values()):
        total_token_freq = total_token_freq + len(postings)
    for postings in list(fr_inversed_index.values()):
        total_token_freq = total_token_freq + len(postings)

    # app run
    app.run()
