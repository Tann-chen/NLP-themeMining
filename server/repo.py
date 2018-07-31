from pymongo import MongoClient

URL = "mongodb://top-theme:uejDPgss76Cxr2VNzKOB19xnf50cWF8ZnHjIVBAJaknlQiBMtuN2vxTszOd7zIDOYkpHBPoPK3EB8hrCPIydfw==@top-theme.documents.azure.com:10255/?ssl=true&replicaSet=globaldb"
DB_NAME = "top-theme"

conn = MongoClient(URL)
db = conn[DB_NAME]
lst_colletion = ["corpus", "queries", "themes", "cluster_analysis", "token_positions", "raw_sentences", "index_en", "index_fr"]


def repo_find_documents(collection_name, dict_criteria):
    if not check_collection_name(collection_name):
        return 0;
    collection = db[collection_name]
    documents = collection.find(dict_criteria)
    return documents


def repo_find_document_by_id(collection_name, _id):
    if not check_collection_name(collection_name):
        return 0;
    collection = db[collection_name]
    documents = collection.find({"_id": _id})
    return list(documents)[0]


def repo_find_all(collection_name):
    if not check_collection_name(collection_name):
        return 0;
    collection = db[collection_name]
    return collection.find()


def repo_count_documents_within_collection(collection_name):
    if not check_collection_name(collection_name):
        return 0;
    collection = db[collection_name]
    return collection.count_documents()


def check_collection_name(collection_name):
    if collection_name not in lst_colletion:
        print("[ERROR] The collection is not existed.")
        return False
    else:
        return True
