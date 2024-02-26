import os

REDIS_CONSTS = {
    "REDIS_HOST": os.getenv("REDIS_HOST", "localhost"),
    "REDIS_PORT": os.getenv("REDIS_PORT", 6379),
    "REDIS_PASSWORD": os.getenv("REDIS_PASSWORD", None),
    "REDIS_STREAM_NAME": os.getenv("REDIS_STREAM_NAME", "scanner_stream")
}