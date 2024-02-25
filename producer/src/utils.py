import uuid
import aioredis
from fastapi import File, UploadFile, HTTPException


async def publish_to_redis(redis, stream, key, content):
    async with redis.pipeline() as pipe:
        await pipe.xadd(stream, {key: content})
        await pipe.execute()

async def handle_file_submission(data: str = None, file: UploadFile = File(None)) -> tuple[uuid.uuid4, bytes]:
    if not data and not file:
        raise HTTPException(status_code=400, detail="No data or file provided")
    key = str(uuid.uuid4())
    if data:
        content = data.encode()
    elif file:
        content = await file.read()
    return key, content

async def get_redis(host: str, port: int, password: str = None):
    return await aioredis.create_redis_pool(f"redis://{host}:{port}", password=password)