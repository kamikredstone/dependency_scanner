import redis

async def get_redis(host: str, port: int, password: str = None) -> redis.ConnectionPool:
    if password:
        pool = redis.ConnectionPool(host=host, port=port, password=password, db=0)
    else:
        pool = redis.ConnectionPool(host=host, port=port, db=0)
    return pool