from typing import List, Optional
from service.net.protocol_base import BaseRequest, BaseResponse

class AccountLoginRequest(BaseRequest):
    id: str
    password: str

class AccountLoginResponse(BaseResponse):
    accessToken: str
    # errorCode, sequence는 BaseResponse에서 상속

class AccountSignupRequest(BaseRequest):
    id: str
    password: str
    name: Optional[str] = None
    phone: Optional[str] = None

class AccountSignupResponse(BaseResponse):
    message: Optional[str] = None
    # errorCode는 BaseResponse에서 상속

class AccountLogoutRequest(BaseRequest):
    pass

class AccountLogoutResponse(BaseResponse):
    pass