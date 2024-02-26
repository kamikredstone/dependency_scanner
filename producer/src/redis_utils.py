import redis

async def publish_to_redis(redis_connection_pool, stream, key, content):
    try:
        r = redis.Redis(connection_pool=redis_connection_pool)
        with r.pipeline() as pipe:
            pipe.xadd(stream, {key: content})
            pipe.execute()
    except Exception as e:
        raise e

async def get_redis(host: str, port: int, password: str = None) -> redis.ConnectionPool:
    if password:
        pool = redis.ConnectionPool(host=host, port=port, passowrd=password, db=0)
    else:
        pool = redis.ConnectionPool(host=host, port=port, db=0)
    return pool