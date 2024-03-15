import logging, sys
import asyncio
from src import REDIS_CONSTS, MONGO_CONSTS
from src.redis_utils import get_redis, ensure_consumer_group_exists, pull_job_from_stream
from src.mongo_utils import get_mongo_collection, process_and_save_message
from pymongo import MongoClient
import redis

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def ensure_str(input_var):
    if isinstance(input_var, bytes):
        return input_var.decode('utf-8')
    return input_var

def listen_for_messages(stream, group_name, consumer_name, mongo_uri, db_name, collection_name, redis_host, redis_port, redis_db):
    redis_pool = get_redis(redis_host, redis_port, REDIS_CONSTS['REDIS_PASSWORD'])
    redis_con = redis.Redis(connection_pool=redis_pool)
    mongo_client = MongoClient(mongo_uri)
    try:
        ensure_consumer_group_exists(redis_pool, stream, group_name)
    except Exception as e:
        logger.error(f"Error creating consumer group: {e}")
        return
    collection = get_mongo_collection(mongo_client, db_name, collection_name)
    while True:
        try:
            messages = pull_job_from_stream(redis_pool, stream, group_name, consumer_name)
            if messages:
                for message in messages:
                    stream, message_data = message
                    message_id = message_data[0][0]
                    logger.debug(f"Processing message from stream: {stream} - containing data: {message_data}")
                    for key, value in message_data[0][1].items():
                        decoded_key = ensure_str(key)
                        decoded_value = ensure_str(value)
                        if key == "init":
                            logger.info("Initialization message received, skipping and acknowledging.")
                            continue
                        process_and_save_message(decoded_key, decoded_value, collection)
                    redis_con.xack(stream, group_name, message_id)
                logger.info(f"Processed messages: {messages}.")
        except Exception as e:
            logger.error(f"Error processing message: {type(e)} - {e}")
            logger.exception("An execption occurred:")

if __name__ == "__main__":
    mongo_uri = f"mongodb://{MONGO_CONSTS['MONGO_HOST']}:{MONGO_CONSTS['MONGO_PORT']}"
    asyncio.run(listen_for_messages(REDIS_CONSTS['REDIS_STREAM_NAME'], 
                                    REDIS_CONSTS['REDIS_GROUP_NAME'], 
                                    REDIS_CONSTS['REDIS_CONSUMER_NAME'], 
                                    mongo_uri, 
                                    MONGO_CONSTS['MONGO_DB'], 
                                    MONGO_CONSTS['MONGO_COLLECTION'], 
                                    REDIS_CONSTS['REDIS_HOST'], 
                                    REDIS_CONSTS['REDIS_PORT'], 0))


