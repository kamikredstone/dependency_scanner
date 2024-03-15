import redis
import logging, sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def get_redis(host: str, port: int, password: str = None) -> redis.ConnectionPool:
    if password:
        pool = redis.ConnectionPool(host=host, port=port, password=password, db=0)
    else:
        pool = redis.ConnectionPool(host=host, port=port, db=0)
    return pool

def pull_job_from_stream(redis_connection_pool, stream, group, consumer, count=1, block=1000):
    try:
        r = redis.Redis(connection_pool=redis_connection_pool)
        return r.xreadgroup(group, consumer, {stream: ">"}, count=count, block=block)
    except Exception as e:
        raise e
    

def ensure_consumer_group_exists(redis_connection_pool, stream, group_name, start='$'):
    try:
        r = redis.Redis(connection_pool=redis_connection_pool)
        # Attempt to create the group. If it already exists, this will throw an error, which we catch.
        try:
            r.xgroup_create(stream, group_name, id=start, mkstream=True)
            logger.info(f"Consumer group '{group_name}' created for stream '{stream}'.")
        except redis.exceptions.ResponseError as e:
            if "BUSYGROUP Consumer Group name already exists" in str(e):
                logger.info(f"Consumer group '{group_name}' already exists for stream '{stream}'.")
            else:
                raise
    except Exception as e:
        raise e