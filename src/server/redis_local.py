import redis

from app import *
from config.databaseconfig import rconf

r = redis.StrictRedis(
    host=rconf["REDIS_HOST"],
    port=rconf["REDIS_PORT"],
    password=rconf["REDIS_PASSWORD"],
    decode_responses=True,
)

