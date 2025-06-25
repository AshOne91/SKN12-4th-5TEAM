from typing import Optional
from service.net.protocol_base import BaseRequest, BaseResponse

class CategoryAskRequest(BaseRequest):
    question: str

class CategoryAskResponse(BaseResponse):
    answer: str 