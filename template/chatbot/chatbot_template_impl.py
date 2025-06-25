from template.base.template.chatbot_template import ChatbotTemplate
from template.chatbot.common.chatbot_serialize import (
    ChatbotAskRequest, ChatbotAskResponse,
    ChatbotRoomsRequest, ChatbotRoomsResponse,
    ChatbotRoomNewRequest, ChatbotRoomNewResponse,
    ChatbotMessageRequest, ChatbotMessageResponse,
    ChatbotHistoryRequest, ChatbotHistoryResponse
)
from template.chatbot.common.chatbot_model import ChatbotRoomInfo, ChatbotMessageHistoryItem
import uuid
from datetime import datetime

class ChatbotTemplateImpl(ChatbotTemplate):
    def init(self, config):
        """챗봇 템플릿 초기화"""
        print("Chatbot template initialized")
        # 임시 방 데이터 저장소 (실제로는 DB 사용)
        self.rooms = {}
        self.messages = {}
        
    def on_load_data(self, config):
        """챗봇 데이터 로딩"""
        print("Chatbot data loaded")
        
    def on_client_create(self, db_client, client_session):
        """클라이언트 생성 시 콜백"""
        print("Chatbot client created")
        
    def on_client_update(self, db_client, client_session):
        """클라이언트 업데이트 시 콜백"""
        print("Chatbot client updated")
        
    def on_client_delete(self, db_client, user_id):
        """클라이언트 삭제 시 콜백"""
        print("Chatbot client deleted")

    async def on_chatbot_ask_req(self, client_session, request: ChatbotAskRequest) -> ChatbotAskResponse:
        # 일반 챗봇 질의 처리
        question = request.question
        # TODO: 실제 챗봇 로직 구현
        answer = f"챗봇 질의: {question}에 대한 응답입니다."
        response = ChatbotAskResponse(answer=answer)
        return response

    async def on_chatbot_rooms_req(self, client_session, request: ChatbotRoomsRequest) -> ChatbotRoomsResponse:
        # 사용자의 채팅방 목록 조회
        user_id = client_session.user_id
        user_rooms = []
        
        # 사용자가 속한 방들 찾기
        for room_id, room_info in self.rooms.items():
            if user_id in room_info.participants:
                user_rooms.append(room_info)
        
        response = ChatbotRoomsResponse(rooms=user_rooms)
        return response

    async def on_chatbot_room_new_req(self, client_session, request: ChatbotRoomNewRequest) -> ChatbotRoomNewResponse:
        # 새 채팅방 생성
        user_id = client_session.user_id
        room_id = str(uuid.uuid4())
        title = request.title or f"새 채팅방 {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        
        # 새 방 정보 생성
        new_room = ChatbotRoomInfo(
            roomId=room_id,
            title=title,
            participants=[user_id],
            createdAt=datetime.now().isoformat()
        )
        
        # 방 저장
        self.rooms[room_id] = new_room
        self.messages[room_id] = []
        
        response = ChatbotRoomNewResponse(roomId=room_id)
        return response

    async def on_chatbot_message_req(self, client_session, request: ChatbotMessageRequest) -> ChatbotMessageResponse:
        # 메시지 전송 및 응답
        user_id = client_session.user_id
        room_id = request.roomId
        message = request.message
        
        # 방 존재 확인
        if room_id not in self.rooms:
            return ChatbotMessageResponse(answer="방을 찾을 수 없습니다.", history=[])
        
        # 사용자가 방에 속해있는지 확인
        if user_id not in self.rooms[room_id].participants:
            return ChatbotMessageResponse(answer="방에 접근할 권한이 없습니다.", history=[])
        
        # 메시지 저장
        message_item = ChatbotMessageHistoryItem(
            messageId=str(uuid.uuid4()),
            userId=user_id,
            message=message,
            timestamp=datetime.now().isoformat(),
            isUser=True
        )
        self.messages[room_id].append(message_item)
        
        # 챗봇 응답 생성
        # TODO: 실제 챗봇 AI 로직 구현
        bot_answer = f"사용자 메시지 '{message}'에 대한 챗봇 응답입니다."
        
        bot_message_item = ChatbotMessageHistoryItem(
            messageId=str(uuid.uuid4()),
            userId="chatbot",
            message=bot_answer,
            timestamp=datetime.now().isoformat(),
            isUser=False
        )
        self.messages[room_id].append(bot_message_item)
        
        response = ChatbotMessageResponse(answer=bot_answer, history=self.messages[room_id])
        return response

    async def on_chatbot_history_req(self, client_session, request: ChatbotHistoryRequest) -> ChatbotHistoryResponse:
        # 대화 이력 조회
        user_id = client_session.user_id
        room_id = request.roomId
        
        # 방 존재 확인
        if room_id not in self.rooms:
            return ChatbotHistoryResponse(history=[])
        
        # 사용자가 방에 속해있는지 확인
        if user_id not in self.rooms[room_id].participants:
            return ChatbotHistoryResponse(history=[])
        
        # 메시지 이력 반환
        history = self.messages.get(room_id, [])
        response = ChatbotHistoryResponse(history=history)
        return response 