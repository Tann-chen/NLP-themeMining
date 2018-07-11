from pymongo import MongoClient

URL = "mongodb://top-theme-mongo:L4SDrxH8M7jk9Z7iotMcx6FxOPLaF6CWkF2ZfUhQKiAK5zN3KqFkQFNVLCsyGNTGapk0RGLZD1YiIuVLQRoC5w==@top-theme-mongo.documents.azure.com:10255/?ssl=true&replicaSet=globaldb"
DB_NAME = "test"

conn = MongoClient(URL)
db = conn[DB_NAME]

lst_colletion = ["corpus", "queries", "themes", "cluster_analysis"]
# get version from db infos
DB_INFOS = db["db_infos"].find({"_id":"DB_INFOS@2018-07-10"})
version = DB_INFOS["version"];
# update version id
NEW_DB_INFOS = DB_INFOS
NEW_DB_INFOS["_id"] = version+0.1
db["db_infos"].update(DB_INFOS, NEW_DB_INFOS)


def insert(collection_name, data):
    if not check_collection_name(collection_name):
        return 0;
    collection = db[collection_name]

    if isinstance(data, list):
        for d in data:
            suffix_id(d)
        collection.insert_many(data)
    if isinstance(data, dict):
        suffix_id(data)
        collection.insert_one(data)


def update(collection_name, old_data, new_data):
    if not check_collection_name(collection_name):
        return 0;
    collection = db[collection_name]
    collection.update(old_data,new_data)


def find_documents(collection_name, dict_criteria):
    if not check_collection_name(collection_name):
        return 0;
    collection = db[collection_name]

    documents = collection.find(dict_criteria)
    reutn documents

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
    return collection.find()


def count_documents_within_collection(collection_name):
    if not check_collection_name(collection_name):
        return 0;
    collection = db[collection_name]
    return collection.count_documents()


def check_collection_name(collection_name):
    if collection_name not in lst_colletion:
        print("[ERROR] The collection is not existed.")
        return False
    else
        return True

def suffix_id(dict):
    if "_id" in dict.keys():
        curr_id = dict["_id"]
        dict["_id"] = curr_id + '@' + version
