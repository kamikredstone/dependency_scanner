import json
from src.parser.python_parser import PythonParser

def get_mongo_collection(client, db_name, collection_name):
    db = client[db_name]
    collection = db[collection_name]
    return collection

def process_and_save_message(key, value, collection):
    # The value is the string we get from redis, which is a JSON string
    value_dict = json.loads(value)
    data = {key: value_dict}

    # Check the key in the JSON and call the correct parser
    for lang, dependencies in value_dict.items():
        if lang == "python":
            parsed_dependencies = PythonParser.parse_dependencies(dependencies)
            data[key] = {'python': parsed_dependencies}

    collection.insert_one(data)