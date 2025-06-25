from typing import Optional
from service.net.protocol_base import BaseRequest, BaseResponse

class ClinicAskRequest(BaseRequest):
    question: str

class ClinicAskResponse(BaseResponse):
    answer: str 