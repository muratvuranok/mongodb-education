# import redis.asyncio as redis
import json

# from core.redis import get_redis
from core.config import settings
import redis.asyncio as redis


redis_client = redis.Redis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True
)


async def set_cache(key: str, value: dict, expire: int = 300):
    data = json.dumps(value)
    await redis_client.set(key, data, ex=expire)


async def get_cache(key: str):
    data = await redis_client.get(key)
    return json.loads(data) if data else None


async def delete_cache(key: str):
    await redis_client.delete(key)


# async def set_cache(key: str, value: dict, expire: int = 300):

#     async for redis_client in get_redis():
#         data = json.dumps(value)
#         await redis_client.set(key, expire, data)


# async def get_cache(key: str):
#     async for redis_client in get_redis():
#         data = await redis_client.get(key)
#         return json.loads(data) if data else None


# async def delete_cache(key: str):
#     async for redis_client in get_redis():
#         await redis_client.delete(key)
