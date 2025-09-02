# Chatbot Template Module

## 📌 모듈 개요
Chatbot 템플릿은 **의료 전문 챗봇 서비스**의 핵심 비즈니스 로직을 구현합니다. 다단계 AI 처리 파이프라인을 통해 정확하고 전문적인 의료 상담 서비스를 제공합니다.

## 🏗️ 실제 구조

```
template/chatbot/
├── chatbot_template_impl.py  # 챗봇 비즈니스 로직 구현
└── common/
    ├── chatbot_model.py     # 데이터 모델
    └── chatbot_serialize.py # 요청/응답 스키마
```

## 🤖 핵심 기능 분석

### 1. 채팅방 관리 시스템

#### 채팅방 목록 조회
```python
async def on_chatbot_rooms_req(self, ...):
    # 샤드 DB에서 사용자별 채팅방 조회
    rows = await userdb_pool.call_procedure("GetChatRoomsByUser", (user_id,))
    rooms = [ChatbotRoomInfo(id=str(row["chat_id"]), title=row["title"]) 
             for row in rows]
```

#### 새 채팅방 생성
```python
async def on_chatbot_room_new_req(self, ...):
    title = request.title or f"새 채팅방 {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    result = await userdb_pool.call_procedure("CreateChatRoom", (user_id, title, None))
    room_id = str(result[0]["p_chat_id"])  # OUT 파라미터에서 ID 추출
```

### 2. 다단계 AI 처리 파이프라인

#### 메시지 처리 플로우
```python
async def on_chatbot_message_req(self, ...):
    # 1. 방 존재 확인 (샤드 DB)
    room_check = await userdb_pool.execute(
        "SELECT chat_id FROM chat_room WHERE user_id = %s AND chat_id = %s"
    )
    
    # 2. 사용자 메시지 저장 (Redis)
    user_message = {
        "role": "user", 
        "content": message, 
        "timestamp": datetime.now().isoformat()
    }
    await save_chat_history(user_id, room_id, user_message)
    
    # 3. 기존 히스토리 로드 (Redis, 최근 10개)
    history = await load_chat_history(user_id, room_id, limit=10)
    
    # 4. 1차 처리: 카테고리 서버 질의
    category_req = CategoryAskRequest(question=message)
    resp = await http_client.post(f"{category_server_url}/category/ask")
    category_answer = resp.json()["answer"]
    
    # 5. 2차 처리: 최종 LLM 호출
    final_answer = await self.call_final_llm(message, category_answer, history)
    
    # 6. 챗봇 응답 저장 (Redis)
    bot_message = {"role": "bot", "content": final_answer, ...}
    await save_chat_history(user_id, room_id, bot_message)
```

### 3. 최종 LLM 처리
```python
async def call_final_llm(self, question, draft_answer, history):
    # 최근 5개 대화 컨텍스트 구성
    context = " ".join([msg["content"] for msg in history[-5:] 
                       if msg.get("role") == "user"])
    
    prompt = f"""
    [사용자 질문] {question}
    [카테고리 전용 LLM 응답] {draft_answer}
    [이전 대화] {context}
    """
    
    # OpenAI GPT-4o-mini 호출
    response = await openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "너는 의료 전문 챗봇이야."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=512
    )
```

## 🔄 전체 아키텍처 플로우

```
사용자 메시지
    ↓
방 존재 확인 (샤드 DB)
    ↓
메시지 저장 (Redis)
    ↓
히스토리 로드 (Redis)
    ↓
카테고리 서버 질의 (HTTP)
    ↓
최종 LLM 호출 (OpenAI)
    ↓
응답 저장 (Redis)
    ↓
최종 응답 반환
```

## 📊 데이터 모델

### 채팅방 정보
```python
class ChatbotRoomInfo(BaseModel):
    id: str      # 채팅방 ID
    title: str   # 채팅방 제목
```

### 메시지 히스토리
```python
class ChatbotMessageHistoryItem(BaseModel):
    role: str     # "user" 또는 "bot"
    content: str  # 메시지 내용
```

### 요청/응답 스키마
- **ChatbotRoomsRequest/Response**: 채팅방 목록 조회
- **ChatbotRoomNewRequest/Response**: 새 채팅방 생성  
- **ChatbotMessageRequest/Response**: 메시지 전송/응답
- **ChatbotHistoryRequest/Response**: 대화 이력 조회

## 🗄️ 데이터 저장 전략

### 1. 샤드 데이터베이스 (MySQL)
```python
# 채팅방 메타데이터
userdb_pool = app.state.userdb_pools[shard_id]
await userdb_pool.call_procedure("GetChatRoomsByUser", (user_id,))
await userdb_pool.call_procedure("CreateChatRoom", (user_id, title, None))
```
**저장 대상**: 채팅방 정보, 사용자-방 매핑

### 2. Redis (캐시)
```python
# 메시지 히스토리 (빠른 조회)
await save_chat_history(user_id, room_id, message)
await load_chat_history(user_id, room_id, limit=10)
```
**저장 대상**: 실시간 대화 내역, 최근 메시지

## 🎯 AI 처리 전략

### 1. 2단계 AI 처리
1. **카테고리 서버**: 도메인 특화 1차 응답 생성
2. **최종 LLM**: 컨텍스트와 히스토리 통합하여 최종 응답

### 2. 컨텍스트 관리
- **최근 히스토리**: 10개 메시지 로드
- **컨텍스트 구성**: 최근 5개 사용자 메시지만 사용
- **토큰 제한**: max_tokens=512로 응답 길이 제한

### 3. 프롬프트 엔지니어링
```python
prompt = f"""
[사용자 질문] {question}
[카테고리 전용 LLM 응답] {draft_answer}  # 1차 처리 결과
[이전 대화] {context}                    # 대화 맥락
"""
```

## 🔐 보안 및 검증

### 1. 권한 검증
```python
# 세션 확인
if client_session is None or not hasattr(client_session, 'user_id'):
    return ChatbotRoomsResponse(rooms=[], errorCode=401)

# 방 소유권 확인
room_check = await userdb_pool.execute(
    "SELECT chat_id FROM chat_room WHERE user_id = %s AND chat_id = %s"
)
```

### 2. 에러 처리
- 카테고리 서버 실패 시 빈 응답으로 처리
- 히스토리 조회 실패 시 빈 배열 반환
- DB/Redis 에러 시 적절한 에러 코드 반환

## 📈 성능 최적화

### 1. 샤딩 활용
```python
shard_id = client_session.shard_id
userdb_pool = app.state.userdb_pools[shard_id]
```
사용자별 샤드 분산으로 DB 부하 분산

### 2. Redis 캐싱
- 채팅 히스토리를 Redis에 저장하여 빠른 조회
- 메시지 제한(10개, 20개)으로 메모리 효율성

### 3. 비동기 처리
- 모든 I/O 작업 (DB, Redis, HTTP, OpenAI) 비동기 처리
- 동시성 향상으로 응답 시간 단축

## ⚠️ 코드에서 발견된 특징

### 강점
1. **다단계 AI 처리**: 전문성과 컨텍스트의 조화
2. **완전한 비동기**: 높은 동시성 지원  
3. **샤딩 지원**: 수평 확장성
4. **히스토리 관리**: 대화 맥락 유지

### 개선 가능 영역
1. **예외 처리**: 일부 try-except 구문의 광범위한 예외 처리
2. **하드코딩**: 토큰 수, 히스토리 수 등 매직 넘버
3. **응답 검증**: OpenAI 응답에 대한 검증 부족

## 🔗 다른 모듈과의 연결

- **service/cache**: 메시지 히스토리 저장/조회
- **service/db**: 채팅방 메타데이터 관리
- **service/http**: 카테고리 서버 통신
- **application/category_server**: 1차 AI 처리
- **OpenAI API**: 최종 LLM 응답 생성

## 🎓 이 모듈에서 배울 수 있는 것

1. **Multi-AI Pipeline**: 여러 AI 모델의 순차적 처리
2. **컨텍스트 관리**: 대화형 AI의 상태 유지
3. **샤딩 실전**: 대규모 채팅 시스템의 데이터 분할
4. **Redis 활용**: 실시간 데이터의 효율적 관리
5. **마이크로서비스 통신**: HTTP를 통한 서비스 간 협력

이 모듈은 **대화형 의료 AI 서비스의 핵심**으로, 복잡한 AI 파이프라인과 실시간 데이터 처리를 조화롭게 구현한 모범 사례입니다.