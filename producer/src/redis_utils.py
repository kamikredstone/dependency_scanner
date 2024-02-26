import redis

async def publish_to_redis(redis, stream, key, content):
    try:
        async with redis.pipeline() as pipe:
            await pipe.xadd(stream, {key: content})
            await pipe.execute()
    except Exception as e:
        raise e

async def get_redis(host: str, port: int, password: str = None):
    if password:
        pool = redis.ConnectionPool(host=host, port=port, passowrd=password, db=0)
    else:
        pool = redis.ConnectionPool(host=host, port=port, db=0)
    return pool