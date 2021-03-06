from pymongo import MongoClient

URL = "mongodb://ec2-18-188-248-132.us-east-2.compute.amazonaws.com:27017/"
DB_NAME = "test"
conn = MongoClient(URL)
db = conn[DB_NAME]

lst_colletion = ["raw_sentences", "corpus", "queries", "themes", "cluster_analysis", "token_positions", "index_en", "index_fr"]


def insert(collection_name, data):
    if not check_collection_name(collection_name):
        return 0

    collection = db[collection_name]

    if isinstance(data, list):
        collection.insert_many(data)

    if isinstance(data, dict):
        collection.insert_one(data)


def find_documents(collection_name, dict_criteria):
    if not check_collection_name(collection_name):
        return 0

    collection = db[collection_name]

    documents = collection.find(dict_criteria)
    return documents


def find_document_by_id(collection_name, _id):
    if not check_collection_name(collection_name):
        return 0

    collection = db[collection_name]

    documents = collection.find({"_id": _id})
    return documents[0]


def find_all(collection_name):
    if not check_collection_name(collection_name):
        return 0
    collection = db[collection_name]
    return collection.find()


def count_documents_within_collection(collection_name):
    if not check_collection_name(collection_name):
        return 0
    collection = db[collection_name]
    return collection.count_documents()


def check_collection_name(collection_name):
    if collection_name not in lst_colletion:
        print("[ERROR] The collection is not existed.")
        return False
    else:
        return True
