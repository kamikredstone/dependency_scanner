from fastapi import FastAPI, File, UploadFile, HTTPException
import os
from utils import publish_to_redis, handle_file_submission, get_redis


app = FastAPI()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)
REDIS_STREAM_NAME = os.getenv("REDIS_STREAM_NAME", "scanner_stream")

@app.post("/submit/")
async def submit_file(data: str = None, file: UploadFile = File(None)):
    redis = await get_redis(REDIS_HOST, REDIS_PORT, REDIS_PASSWORD)
    try:
        key, content = await handle_file_submission(data, file)
        await publish_to_redis(redis, REDIS_STREAM_NAME, key, content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
    finally:
        redis.close()
        await redis.wait_closed()
    return {"message": f"File submitted with key: {key}"}