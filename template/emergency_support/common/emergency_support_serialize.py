from typing import Optional
from service.net.protocol_base import BaseRequest, BaseResponse

class EmergencySupportAskRequest(BaseRequest):
    question: str

class EmergencySupportAskResponse(BaseResponse):
    answer: str 