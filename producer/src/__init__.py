import os

REDIS_CONSTS = {
    "REDIS_HOST": os.getenv("REDIS_HOST", "localhost"),
    "REDIS_PORT": os.getenv("REDIS_PORT", 6379),
    "REDIS_PASSWORD": os.getenv("REDIS_PASSWORD", None),
    "REDIS_STREAM_NAME": os.getenv("REDIS_STREAM_NAME", "scanner_stream"),
    "REDIS_GROUP_NAME": os.getenv("REDIS_GROUP_NAME", "scanner_group") # using the same group as the scanners - the producer consumes only the dummy messages.
}