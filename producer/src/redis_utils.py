import redis
import json
from src.utils import SingletonLogger
import base64

async def publish_to_redis(redis_connection_pool, stream, key, content: dict):
    try:
        r = redis.Redis(connection_pool=redis_connection_pool)
        decoded_content = {}
        for lang, data in content.items():
            if isinstance(data, bytes):
                decoded_data = data.decode('utf-8')
                decoded_content[lang] = decoded_data
            else:
                decoded_content[lang] = data

        with r.pipeline() as pipe:
            pipe.xadd(stream, {key: json.dumps(decoded_content)})
            pipe.execute()
    except Exception as e:
        raise e

async def get_redis(host: str, port: int, password: str = None) -> redis.ConnectionPool:
    if password:
        pool = redis.ConnectionPool(host=host, port=port, password=password, db=0)
    else:
        pool = redis.ConnectionPool(host=host, port=port, db=0)
    return pool

def initialize_stream(redis_connection, stream_name):
    logger = SingletonLogger()
    try:
        latest_entry = redis_connection.xrevrange(stream_name, max='+', min='-', count=1)
        if not latest_entry:
            # Stream is empty or does not exist, safe to add initialization message
            redis_connection.xadd(stream_name, {'init': 'true'})
            logger.info("Stream initialized with dummy message.")
    except redis.exceptions.RedisError as e:
        logger.error(f"Error checking or initializing stream: {e}")
        raise e