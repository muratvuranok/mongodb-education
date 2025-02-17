from fastapi import APIRouter, Depends
from schemas.cache import CacheRequest
from services.cache import set_cache, get_cache, delete_cache

# from core import get_redis

router = APIRouter(prefix="/cache", tags=["Cache"])


@router.post(
    "/set",
    response_model=None,
    status_code=201,
    summary="Set cache",
)
async def set_cached_value(item: CacheRequest):
    await set_cache(item.key, item.value, 300)
    return {"message": "Cache set successfully"}


@router.get(
    "/get/{key}",
    response_model=CacheRequest,
    summary="Get cache",
)
async def get_cached_value(key: str):
    value = await get_cache(key)
    return {"key": key, "value": value}


@router.delete(
    "/delete/{key}",
    response_model=None,
    summary="Delete cache",
)
async def delete_cached_value(key: str):
    await delete_cache(key)
    return {"message": "Cache deleted successfully"}
