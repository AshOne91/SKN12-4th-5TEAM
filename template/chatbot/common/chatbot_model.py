from pydantic import BaseModel

class ChatbotRoomInfo(BaseModel):
    id: str
    title: str

class ChatbotMessageHistoryItem(BaseModel):
    role: str
    content: str