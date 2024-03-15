from fastapi import FastAPI, HTTPException, Request
from src.utils import handle_file_submission
from src.redis_utils import get_redis, publish_to_redis, initialize_stream
from src import REDIS_CONSTS
import logging, sys
import redis

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


## TODO: Think of a better way to initialize the stream
app = FastAPI()
redis_pool = redis.ConnectionPool(host=REDIS_CONSTS['REDIS_HOST'], port=REDIS_CONSTS['REDIS_PORT'], db=0)
redis_con = redis.Redis(connection_pool=redis_pool)
initialize_stream(redis_con, REDIS_CONSTS['REDIS_STREAM_NAME'])
redis_con.close()

## TODO: Write middleware for exception handling
@app.post("/submit/")
async def submit_file(request: Request = None):
    logger.debug(f"Received file submission request with data: {request}")
    r = await get_redis(REDIS_CONSTS['REDIS_HOST'], REDIS_CONSTS['REDIS_PORT'], REDIS_CONSTS['REDIS_PASSWORD'])
    logger.info(f"Connected to Redis at {REDIS_CONSTS['REDIS_HOST']}:{REDIS_CONSTS['REDIS_PORT']}")
    try:
        key, content = await handle_file_submission(request)
        await publish_to_redis(r, REDIS_CONSTS['REDIS_STREAM_NAME'], key, content)
        logger.info(f"Published file with key: {key} to redis stream: {REDIS_CONSTS['REDIS_STREAM_NAME']}")
    except Exception as e:
        logger.error(f"Error occurred while processing file submission: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
    finally:
        r.close()
    return {"message": f"File submitted with key: {key}"}