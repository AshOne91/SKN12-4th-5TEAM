from fastapi import Request, HTTPException
from service.cache.async_session import check_session_info
from service.net.protocol_base import BaseResponse

async def require_session(request: Request):
    # JSON body에서 accessToken 읽기
    body = await request.json()
    access_token = body.get("accessToken")
    if not access_token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    session_info = await check_session_info(access_token)
    if not session_info:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return session_info 