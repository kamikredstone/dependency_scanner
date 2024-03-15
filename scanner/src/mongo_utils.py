def get_mongo_collection(client, db_name, collection_name):
    db = client[db_name]
    collection = db[collection_name]
    return collection

def process_and_save_message(key, value, collection):
    data = {key: value}
    collection.insert_one(data)