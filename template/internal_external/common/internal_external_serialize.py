from typing import Optional
from service.net.protocol_base import BaseRequest, BaseResponse

class InternalExternalAskRequest(BaseRequest):
    question: str

class InternalExternalAskResponse(BaseResponse):
    answer: str 