from fastapi import APIRouter, Depends, Request
from template.base.template_context import TemplateContext
from template.base.template_type import TemplateType
from template.chatbot.common.chatbot_serialize import (
    ChatbotRoomsRequest, ChatbotRoomsResponse,
    ChatbotRoomNewRequest, ChatbotRoomNewResponse,
    ChatbotMessageRequest, ChatbotMessageResponse,
    ChatbotHistoryRequest, ChatbotHistoryResponse
)
from service.cache.dependencies import require_session
from service.net.protocol_base import BaseResponse

router = APIRouter()

@router.post("/rooms", response_model=ChatbotRoomsResponse)
async def chatbot_rooms(request: ChatbotRoomsRequest, req: Request, session=Depends(require_session)):
    if isinstance(session, BaseResponse):
        return session
    chatbot_template = TemplateContext.get_template(TemplateType.CHATBOT)
    if chatbot_template is None:
        raise RuntimeError("ChatbotTemplateImpl is not registered in TemplateContext")
    return await chatbot_template.on_chatbot_rooms_req(session, request, req.app)

@router.post("/room/new", response_model=ChatbotRoomNewResponse)
async def chatbot_room_new(request: ChatbotRoomNewRequest, req: Request, session=Depends(require_session)):
    if isinstance(session, BaseResponse):
        return session
    chatbot_template = TemplateContext.get_template(TemplateType.CHATBOT)
    if chatbot_template is None:
        raise RuntimeError("ChatbotTemplateImpl is not registered in TemplateContext")
    return await chatbot_template.on_chatbot_room_new_req(session, request, req.app)

@router.post("/message", response_model=ChatbotMessageResponse)
async def chatbot_message(request: ChatbotMessageRequest, req: Request, session=Depends(require_session)):
    if isinstance(session, BaseResponse):
        return session
    chatbot_template = TemplateContext.get_template(TemplateType.CHATBOT)
    if chatbot_template is None:
        raise RuntimeError("ChatbotTemplateImpl is not registered in TemplateContext")
    return await chatbot_template.on_chatbot_message_req(session, request, req.app)

@router.post("/history", response_model=ChatbotHistoryResponse)
async def chatbot_history(request: ChatbotHistoryRequest, req: Request, session=Depends(require_session)):
    if isinstance(session, BaseResponse):
        return session
    chatbot_template = TemplateContext.get_template(TemplateType.CHATBOT)
    if chatbot_template is None:
        raise RuntimeError("ChatbotTemplateImpl is not registered in TemplateContext")
    return await chatbot_template.on_chatbot_history_req(session, request, req.app) 