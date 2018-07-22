from pymongo import MongoClient

URL = "mongodb://top-theme:uejDPgss76Cxr2VNzKOB19xnf50cWF8ZnHjIVBAJaknlQiBMtuN2vxTszOd7zIDOYkpHBPoPK3EB8hrCPIydfw==@top-theme.documents.azure.com:10255/?ssl=true&replicaSet=globaldb"
DB_NAME = "top-theme"

conn = MongoClient(URL)
db = conn[DB_NAME]
lst_colletion = ["corpus", "queries", "themes", "cluster_analysis", "token_locations"]

def insert(collection_name, data):
    if not check_collection_name(collection_name):
        return 0;
    collection = db[collection_name]

    if isinstance(data, list):
        collection.insert_many(data)

    if isinstance(data, dict):
        collection.insert_one(data)


def update(collection_name, old_data, new_data):
    if not check_collection_name(collection_name):
        return 0;
    collection = db[collection_name]
    collection.find_one_and_update(old_data,new_data)


def find_documents(collection_name, dict_criteria):
    if not check_collection_name(collection_name):
        return 0;
    collection = db[collection_name]
    dict_criteria["_version"] = version
    documents = collection.find(dict_criteria)
    return documents

def find_document_by_id(collection_name, _id):
    if not check_collection_name(collection_name):
        return 0;
    collection = db[collection_name]
    _id = _id + '@' + str(version)
    documents = collection.find({"_id": _id})
    return documents[0]



def find_all(collection_name):
    if not check_collection_name(collection_name):
        return 0;
    collection = db[collection_name]
    return collection.find({"_version": version})


def count_documents_within_collection(collection_name):
    if not check_collection_name(collection_name):
        return 0;
    collection = db[collection_name]
    return collection.count_documents({"_version": version})


def check_collection_name(collection_name):
    if collection_name not in lst_colletion:
        print("[ERROR] The collection is not existed.")
        return False
    else:
        return True
