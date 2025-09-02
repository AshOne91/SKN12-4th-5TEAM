# Medical AI Chatbot Platform
**(FastAPI 기반 의료 상담 서비스 - 마이크로서비스 아키텍처 구현)**

**TEAM**: 윈도우즈 (5명)  
**MEMBERS**: 권성호, 남의헌, 손현성, 이준배, 이준석  
**PROJECT**: SKN 4차 프로젝트  
**GITHUB**: [https://github.com/SKN12-4th-5TEAM](https://github.com/SKN12-4th-5TEAM)

*의료 접근성 향상을 위한 AI 기반 상담 플랫폼*

---

## ◎ 목 차 ◎

**Ⅰ. 프로젝트 개요**
1. 프로젝트 소개 및 팀 구성
2. 기술 스택 및 개발 환경
3. 핵심 기능 및 서비스 구조

**Ⅱ. 시스템 아키텍처**
1. 6개 마이크로서비스 구조
2. Template 패턴 기반 확장 시스템
3. 데이터베이스 샤딩 및 캐시 전략

**Ⅲ. 핵심 기술 구현**
1. 2단계 LLM 처리 파이프라인
2. RAG 시스템 (FAISS + 한국어 임베딩)
3. 실시간 채팅 히스토리 관리

**Ⅳ. 코드 구현 상세**
1. 템플릿 시스템 구현
2. LLM 통합 및 프롬프트 엔지니어링
3. 비동기 처리 및 성능 최적화

**Ⅴ. 프로젝트 성과 및 회고**
1. 기술적 성과
2. 팀 협업 및 역할
3. 향후 개선 방향

---

## Ⅰ. 프로젝트 개요

### 1. 프로젝트 소개 및 팀 구성

| 항목 | 내용 |
|------|------|
| **프로젝트명** | FastAPI 기반 LLM 연동 의료 서비스 서버 |
| **팀명** | 윈도우즈 |
| **팀원** | 권성호, 남의헌, 손현성, 이준배, 이준석 (5명) |
| **목적** | 의료 관련 LLM 및 다양한 도메인 지식을 연동한 QA/상담 챗봇 개발 |
| **플랫폼** | Web Application (React Frontend + FastAPI Backend) |
| **개발 기간** | 2024년 SKN 4차 프로젝트 |

### 2. 기술 스택 및 개발 환경

| 구분 | 기술 스택 |
|------|-----------|
| **Backend** | Python, FastAPI, uvicorn, LangChain |
| **Database** | MySQL (aiomysql), Redis, Firestore |
| **AI/ML** | OpenAI (gpt-4o-mini), FAISS, jhgan/ko-sroberta-multitask |
| **Message Queue** | RabbitMQ |
| **Frontend** | React, JavaScript |
| **Infrastructure** | AWS, Windows 11, VS Code |

### 3. 핵심 기능 및 서비스 구조

**🎯 주요 기능**
- 의료 도메인별 특화 AI 상담 (약품, 병원, 응급지원 등)
- 2단계 LLM 처리를 통한 정확도 향상
- 실시간 채팅 히스토리 관리
- 사용자 인증 및 세션 관리
- 도메인별 RAG 시스템 구현

---

## Ⅱ. 시스템 아키텍처

### 1. 6개 마이크로서비스 구조

**🏗️ 서비스 구성**

| 서비스명 | 포트 | 역할 | 핵심 기능 |
|---------|------|------|-----------|
| **Chatbot Server** | 8000 | 메인 API 게이트웨이 | 인증, 라우팅, 세션 관리 |
| **Category Server** | 8001 | 카테고리 분류 | 질문 분류, 도메인 라우팅 |
| **Clinic Server** | 8002 | 병원 정보 서비스 | 병원 데이터 조회 |
| **Drug Server** | 8003 | 의약품 정보 서비스 | 약물 정보 RAG 처리 |
| **Emergency Support Server** | 8004 | 응급의료 지원 | 응급 상황 대응 |
| **Internal External Server** | 8005 | 내외부 통신 | 마이크로서비스 간 통신 |

**📡 서비스 간 통신 구조**
```
User Request → Chatbot Server (8000)
            → Category Server (8001) [1차 처리]
            → Domain Service (8002-8005) [특화 처리]
            → Final Response
```

### 2. Template 패턴 기반 확장 시스템

**🎨 Template 계층 구조**
```python
BaseTemplate (추상 클래스)
├── AccountTemplate (사용자 관리)
├── ChatbotTemplate (대화 처리)  
├── CategoryTemplate (카테고리 분류)
├── ClinicTemplate (병원 정보)
├── DrugTemplate (의약품 정보)
├── EmergencyTemplate (응급의료)
└── InternalExternalTemplate (내외부 통신)
```

**💡 BaseTemplate 구현**
```python
# template/base/base_template.py
from abc import ABC, abstractmethod

class BaseTemplate(ABC):
    """모든 템플릿의 기본 추상 클래스"""
    
    @abstractmethod
    def init(self, config):
        """템플릿 초기화"""
        pass
        
    @abstractmethod
    def on_load_data(self, config):
        """데이터 로딩"""
        pass
    
    @abstractmethod  
    def on_client_create(self, db_client, client_session):
        """클라이언트 생성 시 콜백"""
        pass
    
    @abstractmethod
    def on_client_update(self, db_client, client_session):
        """클라이언트 업데이트 시 콜백"""
        pass
    
    @abstractmethod
    def on_client_delete(self, db_client, user_id):
        """클라이언트 삭제 시 콜백"""
        pass
```

### 3. 데이터베이스 샤딩 및 캐시 전략

**🗄️ MySQL 샤딩 구조**
```python
# application/chatbot_server/main.py
@asynccontextmanager
async def lifespan(app: FastAPI):
    # MySQL 샤딩 풀 초기화
    app.state.userdb_pools = {}
    for shard_id in range(NUM_SHARDS):
        pool = MySQLPool()
        await pool.init(
            host=os.getenv(f"DB_SHARD_{shard_id}_HOST"),
            db=f"medichain_shard_{shard_id}"
        )
        app.state.userdb_pools[shard_id] = pool
```

**⚡ Redis 캐시 전략**
- 세션 관리: 1시간 TTL
- 채팅 히스토리: 영구 저장
- LLM 응답 캐싱: 질문별 캐싱

---

## Ⅲ. 핵심 기술 구현

### 1. 2단계 LLM 처리 파이프라인

**🔄 처리 흐름**
```
[사용자 질문]
    ↓
[1차 처리] Category Server (8001)
    - 도메인 분류 (의약품/병원/응급 등)
    - 초안 답변 생성
    ↓
[2차 처리] Chatbot Server (8000)  
    - 히스토리 컨텍스트 추가
    - 최종 답변 생성 (gpt-4o-mini)
    ↓
[응답 저장] Redis
    - 채팅 히스토리 저장
```

**💬 실제 구현 코드**
```python
# template/chatbot/chatbot_template_impl.py
async def on_chatbot_message_req(self, client_session, request, app):
    # 1. Redis에서 대화 히스토리 로드
    history = await load_chat_history(user_id, room_id, limit=10)
    
    # 2. Category Server로 1차 처리
    category_resp = await http_client.post(
        f"{category_server_url}/category/ask",
        json={"question": message}
    )
    category_answer = category_resp.json().get("answer", "")
    
    # 3. 최종 LLM 호출 (gpt-4o-mini)
    final_answer = await self.call_final_llm(
        message, category_answer, history
    )
    
    # 4. Redis에 히스토리 저장
    await save_chat_history(user_id, room_id, bot_message)
    
    return ChatbotMessageResponse(answer=final_answer, history=history_items)
```

### 2. RAG 시스템 구현

**🔍 한국어 특화 RAG 파이프라인**
```python
# service/lang_chain/emergency_support_lang_chain.py

def load_embedding_model():
    """한국어 특화 임베딩 모델"""
    return SentenceTransformer("jhgan/ko-sroberta-multitask")

def build_rag_chain(openai_api_key: str):
    """의료 도메인 RAG 체인"""
    prompt = PromptTemplate.from_template(
        "당신은 의학전공을 하여 저희의 질문에 대답을 잘 해주는 챗봇입니다"
        "다음은 사용자의 질문에 답하기 위한 참고 문서입니다:\n\n"
        "{context}\n\n"
        "질문: {question}\n"
        "답변:"
    )
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    return prompt | llm | StrOutputParser()

async def get_rag_answer_async(question, index, chunks, embed_model, rag_chain):
    # FAISS로 유사 문서 검색
    top_chunks = search_similar_chunks(question, index, chunks, embed_model, top_k=3)
    context = "\n".join(top_chunks)
    
    # LLM으로 답변 생성
    answer = await rag_chain.ainvoke({
        "context": context, 
        "question": question
    })
    return answer
```

**📊 Vector DB 구조**
```
resources/vectorDB/
├── emergency_support_vectorDB/
│   ├── QA_random_pair_part2_chunks1.txt  # 텍스트 청크
│   └── QA_random_pair_part2_index1.index # FAISS 인덱스
└── uiheon/
    ├── QA_random_pair_part1_chunks1.txt
    └── QA_random_pair_part1_index1.index
```

### 3. 실시간 채팅 히스토리 관리

**💾 Redis 기반 히스토리 관리**
```python
# service/cache/async_session.py

async def save_chat_history(user_id: str, room_id: str, message: dict):
    """채팅 메시지 Redis 저장"""
    key = f"chat:{user_id}:{room_id}"
    message["timestamp"] = datetime.now().isoformat()
    await redis_client.lpush(key, json.dumps(message))
    
async def load_chat_history(user_id: str, room_id: str, limit: int = 50):
    """채팅 히스토리 로드"""
    key = f"chat:{user_id}:{room_id}"
    messages = await redis_client.lrange(key, 0, limit-1)
    return [json.loads(msg) for msg in messages]
```

---

## Ⅳ. 코드 구현 상세

### 1. 템플릿 시스템 구현

**🎯 ChatbotTemplate 구현체**
```python
# template/chatbot/chatbot_template_impl.py
class ChatbotTemplateImpl(ChatbotTemplate):
    def init(self, config):
        """챗봇 템플릿 초기화"""
        print("Chatbot template initialized")
        
    async def on_chatbot_rooms_req(self, client_session, request, app):
        """채팅방 목록 조회"""
        user_id = client_session.user_id
        shard_id = client_session.shard_id
        userdb_pool = app.state.userdb_pools[shard_id]
        
        rows = await userdb_pool.call_procedure("GetChatRoomsByUser", (user_id,))
        rooms = [
            ChatbotRoomInfo(
                id=str(row["chat_id"]),
                title=row.get("title", "")
            ) for row in rows
        ] if rows else []
        
        return ChatbotRoomsResponse(rooms=rooms)
    
    async def on_chatbot_room_new_req(self, client_session, request, app):
        """새 채팅방 생성"""
        user_id = client_session.user_id
        shard_id = client_session.shard_id
        userdb_pool = app.state.userdb_pools[shard_id]
        
        title = request.title or f"새 채팅방 {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        result = await userdb_pool.call_procedure("CreateChatRoom", (user_id, title, None))
        room_id = str(result[0]["p_chat_id"])
        
        return ChatbotRoomNewResponse(roomId=room_id)
```

### 2. 데이터베이스 풀 구현

**🔗 MySQL 비동기 풀**
```python
# service/db/database.py
import aiomysql

class MySQLPool:
    def __init__(self):
        self.pool = None

    async def init(self, host, port, user, password, db, minsize=5, maxsize=20):
        self.pool = await aiomysql.create_pool(
            host=host, port=port, 
            user=user, password=password, 
            db=db, minsize=minsize, 
            maxsize=maxsize, autocommit=True
        )

    async def call_procedure(self, proc_name: str, params: tuple = ()): 
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.callproc(proc_name, params)
                result = await cur.fetchall()
                return result

    async def execute(self, query: str, params: tuple = ()): 
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(query, params)
                if query.strip().lower().startswith("select"):
                    return await cur.fetchall()
                return cur.lastrowid
```

### 3. Frontend 통합

**⚛️ React 설정**
```javascript
// frontend/src/config.js
const config = {
    API_BASE_URL: process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000',
    CHATBOT_API_URL: process.env.REACT_APP_CHATBOT_API_URL || 'http://localhost:8000/chatbot',
    ACCOUNT_API_URL: process.env.REACT_APP_ACCOUNT_API_URL || 'http://localhost:8000/account',
    SEQUENCE: parseInt(process.env.REACT_APP_SEQUENCE) || 0,
    DEFAULT_TIMEOUT: parseInt(process.env.REACT_APP_DEFAULT_TIMEOUT) || 30000,
};
```

**🔐 로그인 구현**
```javascript
// frontend/src/Login.js
const handleSubmit = async (e) => {
    e.preventDefault();
    const res = await fetch(`${config.ACCOUNT_API_URL}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            ...form,
            accessToken: "",
            sequence: config.SEQUENCE
        }),
    });
    const data = await res.json();
    if (data.errorCode === 0 && data.accessToken) {
        localStorage.setItem("accessToken", data.accessToken);
        navigate("/chatbot");
    }
};
```

---

## Ⅴ. 프로젝트 성과 및 회고

### 1. 기술적 성과

**✅ 구현 완료 항목**
- 6개 독립 마이크로서비스 구축
- Template 패턴 기반 확장 가능한 아키텍처
- 2단계 LLM 처리로 응답 정확도 향상
- 한국어 특화 RAG 시스템 구현
- MySQL 샤딩 및 Redis 캐싱 전략
- 비동기 처리를 통한 성능 최적화

### 2. 팀 협업 및 역할

**👥 팀원 소감**

| 이름 | 소감 |
|------|------|
| **권성호** | 포기하려 했지만 팀원들 덕분에 끝까지 프로젝트를 완수했습니다. |
| **남의헌** | 서버에 대한 지식을 많이 배워갈 수 있는 시간이었습니다. |
| **손현성** | 이슈가 있었는데 팀원분들 덕분에 프로젝트가 잘 마무리 된 것 같습니다. |
| **이준배** | 다들 포기하지 않고 끝까지 노력한 덕분에 완성할 수 있었습니다. |
| **이준석** | 많이 부족했는데, 다들 많이 신경써주셔서 성공적으로 끝낼 수 있었습니다. |

### 3. 향후 개선 방향

**🔄 개선 계획**
1. **성능 최적화**
   - 응답 시간 단축을 위한 캐싱 전략 고도화
   - 동시 접속자 처리 능력 향상

2. **기능 확장**
   - 의료 이미지 분석 기능 추가
   - 다국어 지원 확대

3. **보안 강화**
   - 의료 정보 암호화 강화
   - HIPAA 컴플라이언스 적용

---

**📁 산출물**
- [요구사항 정의서](./산출물/요구사항%20정의서.hwp)
- [화면설계서](./산출물/화면%20설계서.pdf)
- [테스트 계획 및 결과 보고서](./산출물/테스트계획%20및%20결과보고서.pdf)
- [시스템 구성도](./산출물/5조%20시스템%20아키텍처%20및%20구성도.pdf)

**🏆 프로젝트 의의**

본 프로젝트는 최신 AI 기술과 마이크로서비스 아키텍처를 결합하여 실무급 의료 상담 서비스를 구현했습니다. Template 패턴을 통한 확장성, 2단계 LLM 처리를 통한 정확도, 그리고 한국어 특화 RAG 시스템을 통해 실제 서비스에 적용 가능한 수준의 플랫폼을 구축했습니다.

---

*© 2024 Team 윈도우즈 - SKN 4차 프로젝트*