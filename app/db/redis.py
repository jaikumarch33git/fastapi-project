from redis import StrictRedis


class Redis:
    client: StrictRedis = None


redis_db = Redis()


async def get_redis() -> StrictRedis:
    return redis_db.client
