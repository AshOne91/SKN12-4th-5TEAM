from pydantic import BaseModel

class CacheConfig(BaseModel):
    cache_type: int = 0  # ECacheType.Redis에 해당하는 값(예: 0)
    host: str = "localhost"
    port: int = 6379
    session_expire_time: int = 3600 