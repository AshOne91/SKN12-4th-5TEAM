from fastapi import APIRouter
from service.cache.async_session import set_session_info, get_session_info
from template.base.session_info import SessionInfo, ClientSessionState

router = APIRouter()

@router.get("/test_set_session")
async def test_set_session():
    await set_session_info("foo", SessionInfo(user_id="bar", session_state=ClientSessionState.NONE))
    return {"result": "ok"}

@router.get("/test_get_session")
async def test_get_session():
    session = await get_session_info("foo")
    return {"session": session.user_id if session else None}
