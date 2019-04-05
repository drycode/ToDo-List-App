import redis

from server.redis.redis_config import *

redis_instance = redis.StrictRedis(
    host=rconf["REDIS_HOST"],
    port=rconf["REDIS_PORT"],
    password=rconf["REDIS_PASSWORD"],
    decode_responses=True,
)

