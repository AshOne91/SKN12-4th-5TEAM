from typing import List, Optional
from service.net.protocol_base import BaseRequest, BaseResponse
from template.chatbot.common.chatbot_model import *

# 채팅방 목록
class ChatbotRoomsRequest(BaseRequest):
    pass

class ChatbotRoomsResponse(BaseResponse):
    rooms: List[ChatbotRoomInfo]

# 채팅방 생성
class ChatbotRoomNewRequest(BaseRequest):
    title: Optional[str] = None

class ChatbotRoomNewResponse(BaseResponse):
    roomId: str

# 메시지 전송
class ChatbotMessageRequest(BaseRequest):
    roomId: str
    message: str

class ChatbotMessageResponse(BaseResponse):
    answer: str
    history: Optional[List[ChatbotMessageHistoryItem]] = None

# 대화 이력 조회
class ChatbotHistoryRequest(BaseRequest):
    roomId: str

class ChatbotHistoryResponse(BaseResponse):
    history: List[ChatbotMessageHistoryItem] 