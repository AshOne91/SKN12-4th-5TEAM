import redis
import json
from fastapi_base_server.template.base.session_info import SessionInfo, ClientSessionState

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

SESSION_EXPIRE_MINUTES = 60

def set_session_info(access_token: str, session_info: SessionInfo):
    r.setex(f"accessToken:{access_token}", SESSION_EXPIRE_MINUTES*60, session_info.platform_id)
    r.setex(f"sessionInfo:{access_token}", SESSION_EXPIRE_MINUTES*60, json.dumps(session_info.__dict__))

def get_session_info(access_token: str) -> SessionInfo | None:
    session_json = r.get(f"sessionInfo:{access_token}")
    if not session_json:
        return None
    data = json.loads(session_json)
    return SessionInfo(**data)

def remove_session_info(access_token: str):
    r.delete(f"accessToken:{access_token}")
    r.delete(f"sessionInfo:{access_token}")

def check_session_info(access_token: str) -> SessionInfo | None:
    session_info = get_session_info(access_token)
    if not session_info:
        return None
    # 만료 갱신 (옵션)
    r.expire(f"accessToken:{access_token}", SESSION_EXPIRE_MINUTES*60)
    r.expire(f"sessionInfo:{access_token}", SESSION_EXPIRE_MINUTES*60)
    if session_info.session_state != ClientSessionState.NONE:
        return None
    return session_info 