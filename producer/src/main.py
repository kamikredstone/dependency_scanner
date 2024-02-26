from fastapi import FastAPI, File, UploadFile, HTTPException
from utils import publish_to_redis, handle_file_submission, get_redis
from src import REDIS_CONSTS


app = FastAPI()

@app.post("/submit/")
async def submit_file(data: str = None, file: UploadFile = File(None)):
    redis = await get_redis(REDIS_CONSTS.REDIS_HOST, REDIS_CONSTS.REDIS_PORT, REDIS_CONSTS.REDIS_PASSWORD)
    try:
        key, content = await handle_file_submission(data, file)
        await publish_to_redis(redis, REDIS_CONSTS.REDIS_STREAM_NAME, key, content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
    finally:
        redis.close()
        await redis.wait_closed()
    return {"message": f"File submitted with key: {key}"}