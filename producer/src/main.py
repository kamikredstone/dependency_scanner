from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from src.utils import handle_file_submission
from src.redis_utils import get_redis, publish_to_redis
from src import REDIS_CONSTS
import logging, sys


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

app = FastAPI()

## TODO: Write middleware for exception handling
@app.post("/submit/")
async def submit_file(request: Request = None):
    logger.debug(f"Received file submission request with data: {request}")
    redis = await get_redis(REDIS_CONSTS['REDIS_HOST'], REDIS_CONSTS['REDIS_PORT'], REDIS_CONSTS['REDIS_PASSWORD'])
    logger.info(f"Connected to Redis at {REDIS_CONSTS['REDIS_HOST']}:{REDIS_CONSTS['REDIS_PORT']}")
    try:
        key, content = await handle_file_submission(request)
        await publish_to_redis(redis, REDIS_CONSTS['REDIS_STREAM_NAME'], key, content)
        logger.info(f"Published file with key: {key} to redis stream: {REDIS_CONSTS['REDIS_STREAM_NAME']}")
    except Exception as e:
        logger.error(f"Error occurred while processing file submission: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
    finally:
        redis.close()
    return {"message": f"File submitted with key: {key}"}