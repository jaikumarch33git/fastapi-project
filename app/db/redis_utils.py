import logging

import redis
from app.db.redis import redis_db
from ..core.config import REDIS_HOST, REDIS_PORT, REDIS_DB


def connect_to_redis():
    logging.info("Connect to the redis...")
    redis_db.client = redis.StrictRedis.from_url("redis://{}:{}/".format(REDIS_HOST, REDIS_PORT),db=REDIS_DB,
                                              decode_responses=True)
    logging.info("Connected to the redis successfully !")


def close_redis_connection():
    logging.info("Close the redis connection...")
    redis_db.client.close()
    logging.info("Redis connection is closed！")
