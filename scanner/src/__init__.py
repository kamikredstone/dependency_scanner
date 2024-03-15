import os
import uuid

REDIS_CONSTS = {
    "REDIS_HOST": os.getenv("REDIS_HOST", "localhost"),
    "REDIS_PORT": os.getenv("REDIS_PORT", 6379),
    "REDIS_PASSWORD": os.getenv("REDIS_PASSWORD", None),
    "REDIS_STREAM_NAME": os.getenv("REDIS_STREAM_NAME", "scanner_stream"),
    "REDIS_GROUP_NAME": os.getenv("REDIS_GROUP_NAME", "scanner_group"),
    "REDIS_CONSUMER_NAME": os.getenv("REDIS_CONSUMER_NAME", str(uuid.uuid4())),
}

MONGO_CONSTS = {
    "MONGO_HOST": os.getenv("MONGO_HOST", "localhost"),
    "MONGO_PORT": os.getenv("MONGO_PORT", 27017),
    "MONGO_DB": os.getenv("MONGO_DB", "scanner"),
    "MONGO_COLLECTION": os.getenv("MONGO_COLLECTION", "dependencies"),
}