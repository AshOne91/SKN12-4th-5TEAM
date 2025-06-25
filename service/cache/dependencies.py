from fastapi import Request
from service.cache.async_session import check_session_info
from service.net.protocol_base import BaseResponse

async def require_session(request: Request):
    access_token = request.headers.get("Authorization")
    if not access_token:
        return BaseResponse(errorCode=401)
    session_info = await check_session_info(access_token)
    if not session_info:
        return BaseResponse(errorCode=401)
    return session_info 