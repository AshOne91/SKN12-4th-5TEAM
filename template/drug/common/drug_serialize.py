from typing import Optional
from service.net.protocol_base import BaseRequest, BaseResponse

class DrugAskRequest(BaseRequest):
    question: str

class DrugAskResponse(BaseResponse):
    answer: str 