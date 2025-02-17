from pydantic import BaseModel


class CacheRequest(BaseModel):
    key: str
    value: dict
