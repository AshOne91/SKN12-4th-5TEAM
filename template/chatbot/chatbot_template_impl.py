from template.base.template.chatbot_template import ChatbotTemplate
from template.chatbot.common.chatbot_serialize import (
    ChatbotRoomsRequest, ChatbotRoomsResponse,
    ChatbotRoomNewRequest, ChatbotRoomNewResponse,
    ChatbotMessageRequest, ChatbotMessageResponse,
    ChatbotHistoryRequest, ChatbotHistoryResponse
)
from template.chatbot.common.chatbot_model import ChatbotRoomInfo, ChatbotMessageHistoryItem
import uuid
from datetime import datetime
import json
from service.cache.async_session import save_chat_history, load_chat_history
import openai
from template.category.common.category_serialize import CategoryAskRequest, CategoryAskResponse
from dotenv import load_dotenv

import os
print("OPENAI_API_KEY:", os.getenv("OPENAI_API_KEY"))

# openai.AsyncOpenAI 인스턴스 생성
openai_client = openai.AsyncOpenAI()

# Load environment variables from .env file
load_dotenv()

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

    async def on_chatbot_rooms_req(self, client_session, request: ChatbotRoomsRequest, app) -> ChatbotRoomsResponse:
        try:
            if client_session is None or not hasattr(client_session, 'user_id'):
                # 인증 실패 등
                return ChatbotRoomsResponse(rooms=[], errorCode=401, sequence=0)
            user_id = client_session.user_id
            shard_id = client_session.shard_id
            userdb_pool = app.state.userdb_pools[shard_id]
            rows = await userdb_pool.call_procedure("GetChatRoomsByUser", (user_id,))
            rooms = [
                ChatbotRoomInfo(
                    id=str(row["chat_id"]),
                    title=row.get("title", ""),
                )
                for row in rows
            ] if rows else []
            return ChatbotRoomsResponse(rooms=rooms)
        except Exception as e:
            return ChatbotRoomsResponse(rooms=[], errorCode=500, sequence=0)

    async def on_chatbot_room_new_req(self, client_session, request: ChatbotRoomNewRequest, app) -> ChatbotRoomNewResponse:
        # 새 채팅방 생성
        user_id = client_session.user_id
        shard_id = client_session.shard_id
        userdb_pool = app.state.userdb_pools[shard_id]
        title = request.title or f"새 채팅방 {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        
        # 샤드DB에 채팅방 생성 프로시저 호출 (OUT 파라미터 사용)
        result = await userdb_pool.call_procedure("CreateChatRoom", (user_id, title, None))
        # result에서 chat_id 추출 (프로시저의 OUT 파라미터)
        room_id = str(result[0]["p_chat_id"])
        
        return ChatbotRoomNewResponse(roomId=room_id)

    async def on_chatbot_message_req(self, client_session, request: ChatbotMessageRequest, app) -> ChatbotMessageResponse:
        user_id = client_session.user_id
        room_id = request.roomId
        message = request.message
        shard_id = client_session.shard_id
        userdb_pool = app.state.userdb_pools[shard_id]
        http_client = app.state.http_client
        category_server_url = app.state.category_server_url

        # 1. DB에서 방 존재 확인
        room_check = await userdb_pool.execute(
            "SELECT chat_id FROM chat_room WHERE user_id = %s AND chat_id = %s",
            (user_id, room_id)
        )
        if not room_check or len(room_check) == 0:
            return ChatbotMessageResponse(answer="채팅방을 찾을 수 없습니다.", history=[])

        # 2. 사용자 메시지를 Redis 히스토리에 저장
        user_message = {
            "role": "user",
            "content": message,
            "timestamp": datetime.now().isoformat()
        }
        await save_chat_history(user_id, room_id, user_message)

        # 3. 기존 히스토리 로드
        history = await load_chat_history(user_id, room_id, limit=10)

        # 4. 카테고리 서버에 질의 (질문, 히스토리 등 전달)
        try:
            category_req = CategoryAskRequest(question=message)
            resp = await http_client.post(
                f"{category_server_url}/category/ask",
                json=category_req.model_dump()
            )
            resp.raise_for_status()
            category_resp_json = await resp.json()
            category_answer = category_resp_json.get("answer", "")
        except Exception as e:
            print(f"카테고리 서버 질의 실패: {e}")
            category_answer = ""

        # 5. 최종 LLM 호출 (질문, draft_answer, 히스토리)
        final_answer = await self.call_final_llm(message, category_answer, history)

        # 6. 챗봇 응답을 Redis 히스토리에 저장
        bot_message = {
            "role": "bot",
            "content": final_answer,
            "timestamp": datetime.now().isoformat()
        }
        await save_chat_history(user_id, room_id, bot_message)

        # 7. 최신 히스토리 반환
        updated_history = await load_chat_history(user_id, room_id, limit=20)
        # 각 dict가 반드시 role, content 키를 갖도록 변환
        history_items = [
            {"role": item.get("role", ""), "content": item.get("content", "")}
            for item in updated_history
        ]
        return ChatbotMessageResponse(answer=final_answer, history=history_items)

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
            history = await load_chat_history(user_id, room_id, limit=50)
            # ChatbotMessageHistoryItem 형태로 변환
            history_items = []
            for item in history:
                history_items.append(ChatbotMessageHistoryItem(
                    role=item.get("role", ""),
                    content=item.get("content", "")
                ))
            return ChatbotHistoryResponse(history=history_items)
        except Exception as e:
            print(f"히스토리 조회 실패: {e}")
            return ChatbotHistoryResponse(history=[])

    async def call_final_llm(self, question: str, draft_answer: str, history: list) -> str:
        """최종 LLM 호출 (카테고리, draft_answer, 히스토리 포함)"""
        # 히스토리 context 구성
        context = ""
        if history:
            recent_messages = history[-5:]
            context = " ".join([msg["content"] for msg in recent_messages if msg.get("role") == "user"])

        # 프롬프트 구성
        prompt = f"""
        [사용자 질문]
        {question}

        [카테고리 전용 LLM 응답]
        {draft_answer}

        [이전 대화]
        {context}

        [최종 응답]
        """

        # 실제 LLM 호출 (예: OpenAI)
        response = await openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "너는 의료 전문 챗봇이야. 아래 정보를 참고해서 답변해."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=512
        )
        return response.choices[0].message.content or ""