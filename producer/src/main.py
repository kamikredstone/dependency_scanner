from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from src.utils import handle_file_submission
from src.redis_utils import get_redis, publish_to_redis
from src import REDIS_CONSTS

app = FastAPI()

## TODO: Write middleware for exception handling
@app.post("/submit/")
async def submit_file(data: Request = None, file: UploadFile = File(None)):
    redis = await get_redis(REDIS_CONSTS['REDIS_HOST'], REDIS_CONSTS['REDIS_PORT'], REDIS_CONSTS['REDIS_PASSWORD'])
    try:
        key, content = await handle_file_submission(data, file)
        await publish_to_redis(redis, REDIS_CONSTS['REDIS_STREAM_NAME'], key, content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
    finally:
        redis.close()
    return {"message": f"File submitted with key: {key}"}