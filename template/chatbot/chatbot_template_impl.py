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
import json
from service.cache.async_session import r, _check_init

class ChatbotTemplateImpl(ChatbotTemplate):
    def init(self, config):
        """챗봇 템플릿 초기화"""
        print("Chatbot template initialized")
        # 웹서버에서는 임시 메모리 저장 불필요
        # 모든 데이터는 DB/Redis에 저장

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

    async def on_chatbot_ask_req(self, client_session, request: ChatbotAskRequest, app) -> ChatbotAskResponse:
        question = request.question
        http_client = app.state.http_client
        category_server_url = app.state.category_server_url

        # 1. 카테고리 분류 서버에 요청
        resp = await http_client.post(
            f"{category_server_url}/classify",
            json={"text": question}
        )
        resp.raise_for_status()
        category = (await resp.json())["category"]

        # 2. (예시) LLM 호출 - 실제로는 history/context 등도 함께 전달
        # answer = await call_llm(question, category, ...)
        answer = f"[카테고리: {category}] 질문: {question}에 대한 응답입니다."

        return ChatbotAskResponse(answer=answer)

    async def on_chatbot_rooms_req(self, client_session, request: ChatbotRoomsRequest, app) -> ChatbotRoomsResponse:
        user_id = client_session.user_id
        shard_id = client_session.shard_id
        userdb_pool = app.state.userdb_pools[shard_id]

        # 샤드DB에서 프로시저 호출
        rows = await userdb_pool.call_procedure("GetChatRoomsByUser", (user_id,))
        # rows는 DictCursor 반환값

        # ChatbotRoomInfo로 변환
        rooms = [
            ChatbotRoomInfo(
                id=str(row["chat_id"]),
                title=row.get("title", ""),
            )
            for row in rows
        ]
        return ChatbotRoomsResponse(rooms=rooms)

    async def on_chatbot_room_new_req(self, client_session, request: ChatbotRoomNewRequest, app) -> ChatbotRoomNewResponse:
        # 새 채팅방 생성
        user_id = client_session.user_id
        shard_id = client_session.shard_id
        userdb_pool = app.state.userdb_pools[shard_id]
        title = request.title or f"새 채팅방 {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        
        # 샤드DB에 채팅방 생성 프로시저 호출 (OUT 파라미터 사용)
        result = await userdb_pool.call_procedure("CreateChatRoom", (user_id, title, None))
        # result에서 chat_id 추출 (프로시저의 OUT 파라미터)
        room_id = str(result[0]["p_chat_id"]) if result and len(result) > 0 else str(uuid.uuid4())
        
        return ChatbotRoomNewResponse(roomId=room_id)

    async def on_chatbot_message_req(self, client_session, request: ChatbotMessageRequest, app) -> ChatbotMessageResponse:
        """메시지 전송 및 응답 처리"""
        user_id = client_session.user_id
        room_id = request.roomId
        message = request.message
        shard_id = client_session.shard_id
        userdb_pool = app.state.userdb_pools[shard_id]
        http_client = app.state.http_client
        category_server_url = app.state.category_server_url

        # 1. DB에서 방 존재 확인 (직접 쿼리 사용)
        room_check = await userdb_pool.execute(
            "SELECT chat_id FROM chat_room WHERE user_id = %s AND chat_id = %s",
            (user_id, room_id)
        )
        if not room_check or len(room_check) == 0:
            return ChatbotMessageResponse(answer="채팅방을 찾을 수 없습니다.", history=[])

        # 2. 사용자 메시지를 Redis 히스토리에 저장
        user_message = {
            "type": "user",
            "content": message,
            "timestamp": datetime.now().isoformat()
        }
        await self.save_chat_history(user_id, room_id, user_message)

        # 3. 기존 히스토리 로드 (컨텍스트용)
        history = await self.load_chat_history(user_id, room_id, limit=10)

        # 4. 카테고리 분류 서버에 요청
        try:
            resp = await http_client.post(
                f"{category_server_url}/classify",
                json={"text": message}
            )
            resp.raise_for_status()
            category = (await resp.json())["category"]
        except Exception as e:
            print(f"카테고리 분류 실패: {e}")
            category = "general"

        # 5. LLM 호출 (실제 구현에서는 실제 LLM API 호출)
        # TODO: 실제 LLM API 연동
        bot_answer = await self.call_llm(message, category, history)

        # 6. 챗봇 응답을 Redis 히스토리에 저장
        bot_message = {
            "type": "bot",
            "content": bot_answer,
            "timestamp": datetime.now().isoformat()
        }
        await self.save_chat_history(user_id, room_id, bot_message)

        # 7. 최신 히스토리 반환
        updated_history = await self.load_chat_history(user_id, room_id, limit=20)
        
        return ChatbotMessageResponse(answer=bot_answer, history=updated_history)

    async def on_chatbot_history_req(self, client_session, request: ChatbotHistoryRequest, app) -> ChatbotHistoryResponse:
        """채팅 히스토리 조회"""
        user_id = client_session.user_id
        room_id = request.roomId
        shard_id = client_session.shard_id
        userdb_pool = app.state.userdb_pools[shard_id]

        # 1. DB에서 방 존재 확인 (직접 쿼리 사용)
        room_check = await userdb_pool.execute(
            "SELECT chat_id FROM chat_room WHERE user_id = %s AND chat_id = %s",
            (user_id, room_id)
        )
        if not room_check or len(room_check) == 0:
            return ChatbotHistoryResponse(history=[])

        # 2. Redis에서 히스토리 조회 (기본 50개)
        try:
            history = await self.load_chat_history(user_id, room_id, limit=50)
            
            # ChatbotMessageHistoryItem 형태로 변환
            history_items = []
            for item in history:
                history_items.append(ChatbotMessageHistoryItem(
                    role=item["type"],  # type을 role로 매핑
                    content=item["content"]
                ))
            
            return ChatbotHistoryResponse(history=history_items)
        except Exception as e:
            print(f"히스토리 조회 실패: {e}")
            return ChatbotHistoryResponse(history=[])

    async def call_llm(self, question: str, category: str, history: list) -> str:
        """실제 LLM 호출 (현재는 모의 응답)"""
        # TODO: 실제 LLM API 연동 (OpenAI, Claude 등)
        # 현재는 카테고리와 히스토리를 고려한 모의 응답
        
        # 히스토리에서 컨텍스트 추출
        context = ""
        if history:
            recent_messages = history[-5:]  # 최근 5개 메시지만 사용
            context = " ".join([msg["content"] for msg in recent_messages if msg["type"] == "user"])
        
        # 카테고리별 응답 생성
        category_responses = {
            "medicine": f"약물 관련 질문 '{question}'에 대한 전문적인 답변입니다. {context}",
            "treatment": f"치료 관련 질문 '{question}'에 대한 의학적 조언입니다. {context}",
            "symptom": f"증상 관련 질문 '{question}'에 대한 분석입니다. {context}",
            "general": f"일반적인 의료 질문 '{question}'에 대한 답변입니다. {context}"
        }
        
        return category_responses.get(category, category_responses["general"])

    async def save_chat_history(self, user_id: str, room_id: str, message: dict):
        """Redis에 채팅 히스토리 저장"""
        _check_init()
        key = f"chat_history:{user_id}:{room_id}"
        await r.rpush(key, json.dumps(message))
        # 최대 50개 메시지 유지
        await r.ltrim(key, -50, -1)

    async def load_chat_history(self, user_id: str, room_id: str, limit: int = 20):
        """Redis에서 채팅 히스토리 조회"""
        _check_init()
        key = f"chat_history:{user_id}:{room_id}"
        history = await r.lrange(key, -limit, -1)
        return [json.loads(m) for m in history] 