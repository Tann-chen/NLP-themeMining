from pymongo import MongoClient

URL = "mongodb://top-theme:uejDPgss76Cxr2VNzKOB19xnf50cWF8ZnHjIVBAJaknlQiBMtuN2vxTszOd7zIDOYkpHBPoPK3EB8hrCPIydfw==@top-theme.documents.azure.com:10255/?ssl=true&replicaSet=globaldb"
DB_NAME = "top-theme"

conn = MongoClient(URL)
db = conn[DB_NAME]

lst_colletion = ["corpus", "queries", "themes", "cluster_analysis", "token_locations"]
# get version from db infos
DB_INFOS = db["db_infos"].find({"_id":"DB_INFOS@2018-07-10"})[0]
version = DB_INFOS["version"]-1
print("[INFO] The version of data :" + str(version))



def repo_find_documents(collection_name, dict_criteria):
    if not check_collection_name(collection_name):
        return 0;
    collection = db[collection_name]
    dict_criteria["_version"] = version
    documents = collection.find(dict_criteria)
    return documents


def repo_find_document_by_id(collection_name, _id, attach_version=False):
    if not check_collection_name(collection_name):
        return 0;
    collection = db[collection_name]
    if attach_version:
        _id = str(_id) + '@' + str(version)
    documents = collection.find({"_id": _id})
    return list(documents)[0]


def repo_find_all(collection_name):
    if not check_collection_name(collection_name):
        return 0;
    collection = db[collection_name]
    return collection.find({"_version": version})


def repo_count_documents_within_collection(collection_name):
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

def suffix_id(dict):
    if "_id" in dict.keys():
        curr_id = dict["_id"]
        dict["_id"] = curr_id + '@' + version
