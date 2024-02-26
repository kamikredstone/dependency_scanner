import uuid
import redis
from fastapi import File, UploadFile, HTTPException


async def publish_to_redis(redis, stream, key, content):
    async with redis.pipeline() as pipe:
        await pipe.xadd(stream, {key: content})
        await pipe.execute()

async def handle_file_submission(data: str = None, file: UploadFile = None) -> tuple[uuid.uuid4, bytes]:
    if data == None and file == None:
        raise HTTPException(status_code=400, detail="No data or file provided")
    key = str(uuid.uuid4())
    if data:
        content = data.encode()
    elif file:
        file.seek(0)
        content = await file.read()
    return key, content

async def get_redis(host: str, port: int, password: str = None):
    if password:
        pool = redis.ConnectionPool(host=host, port=port, passowrd=password, db=0)
    else:
        pool = redis.ConnectionPool(host=host, port=port, db=0)
    return pool