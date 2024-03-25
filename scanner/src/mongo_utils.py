import json
from src.parser.python_parser import PythonParser

def get_mongo_collection(client, db_name, collection_name):
    db = client[db_name]
    collection = db[collection_name]
    return collection

def process_and_save_message(key: str, value: str, collection):
    """
    Args:
        key (str): The key of the message, which is a UUID identifier.
        value (str): The value of the message, which is a JSON string, where the key is the programming language and the value is the manifest file content.
        collection (pymongo.collection.Collection): The MongoDB collection to save the data to.

    This function takes the manifest file from the Redis stream and processes it,
    Creating a dependency tree and saving it to the MongoDB collection as a JSON.
    In the future it will instead process the JSON and produce a vulnerability report,
    saving it in the collection.
    """
    # The value is the string we get from redis, which is a JSON string
    value_dict = json.loads(value)
    data = {}

    # Check the key in the JSON and call the correct parser
    for lang, dependencies in value_dict.items():
        if lang == "python":
            parsed_dependencies = PythonParser.parse_dependencies(dependencies)
            for dep in parsed_dependencies:
                package_name = dep['name']
                package_version = dep['specs'][0][1]
                tree = PythonParser.build_dependency_tree(package_name, package_version)
            data[key] = {'python': tree}

    collection.insert_one(data)