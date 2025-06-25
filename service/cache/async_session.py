import redis.asyncio as redis
import json
from typing import Optional
from template.base.session_info import SessionInfo, ClientSessionState
from service.cache.cache_config import CacheConfig

r: Optional[redis.Redis] = None
SESSION_EXPIRE_MINUTES = 60

def init_cache(config: CacheConfig):
    global r, SESSION_EXPIRE_MINUTES
    r = redis.Redis(host=config.host, port=config.port, db=0, decode_responses=True)
    SESSION_EXPIRE_MINUTES = config.session_expire_time // 60 if config.session_expire_time else 60

def _check_init():
    if r is None:
        raise RuntimeError("Redis client is not initialized. Call init_cache first.")

async def set_session_info(access_token: str, session_info: SessionInfo):
    _check_init()
    await r.setex(f"accessToken:{access_token}", SESSION_EXPIRE_MINUTES*60, session_info.platform_id)
    await r.setex(f"sessionInfo:{access_token}", SESSION_EXPIRE_MINUTES*60, json.dumps(session_info.__dict__))

async def get_session_info(access_token: str) -> SessionInfo | None:
    _check_init()
    session_json = await r.get(f"sessionInfo:{access_token}")
    if not session_json:
        return None
    data = json.loads(session_json)
    return SessionInfo(**data)

async def remove_session_info(access_token: str):
    _check_init()
    await r.delete(f"accessToken:{access_token}")
    await r.delete(f"sessionInfo:{access_token}")

async def check_session_info(access_token: str) -> SessionInfo | None:
    _check_init()
    session_info = await get_session_info(access_token)
    if not session_info:
        return None
    await r.expire(f"accessToken:{access_token}", SESSION_EXPIRE_MINUTES*60)
    await r.expire(f"sessionInfo:{access_token}", SESSION_EXPIRE_MINUTES*60)
    if session_info.session_state != ClientSessionState.NONE:
        return None
    return session_info 