# Medical AI Chatbot Platform
## 팀: 윈도우즈 | 팀원: 권성호, 남의헌, 손현성, 이준배, 이준석 | 파트: 백엔드 아키텍처

---

## ◎ 목 차 ◎

**Ⅰ. 포트폴리오 개요** ··················································· 3
   1. Medical AI Chatbot Platform 개요 ································ 3
   2. 개발 환경 및 사용 기술 ········································· 4
   3. 프로젝트 주요 특징 ············································· 5

**Ⅱ. 기술 요약 및 UML** ·················································· 6
   1. 시스템 아키텍처 ················································ 6
   2. 핵심 기능 다이어그램 ··········································· 8
   3. 클래스 다이어그램 ·············································· 10

**Ⅲ. 별첨 (기술 구현 상세)** ············································· 12
   1. FastAPI 마이크로서비스 구현 ···································· 12
   2. LLM/RAG 통합 시스템 ············································ 15
   3. Template Pattern 구현 ·········································· 18

---

## Ⅰ. 포트폴리오 개요

### 1. Medical AI Chatbot Platform 개요

| 구분 | 내용 |
|------|------|
| **프로젝트명** | Medical AI Chatbot Platform |
| **개발 기간** | 2024년 (SKN 4차 프로젝트) |
| **개발 인원** | 5명 (팀 프로젝트) |
| **담당 역할** | 백엔드 아키텍처 설계 및 구현 |
| **플랫폼** | Web Application |
| **장르** | AI 의료 상담 서비스 |
| **사용 기술** | Python, FastAPI, LangChain, OpenAI, React |
| **데이터베이스** | MySQL, Firestore, Redis |

**프로젝트 개요**
의료 접근성 향상을 위한 AI 기반 상담 플랫폼으로, FastAPI 마이크로서비스 아키텍처와 LLM/RAG 기술을 통합하여 구현했습니다. Template Pattern을 적용한 확장 가능한 구조로 다양한 의료 도메인에 대응 가능합니다.

**GitHub**: https://github.com/SKN12-4th-5TEAM

### 2. 개발 환경 및 사용 기술

#### 2.1 개발 환경

| 구분 | 사양 |
|------|------|
| **OS** | Windows 11, Ubuntu 22.04 |
| **IDE** | VS Code, PyCharm |
| **Language** | Python 3.11, JavaScript ES6+ |
| **Framework** | FastAPI 0.115.6, React 18.2.0 |
| **Database** | MySQL 8.0, Firestore, Redis 7.2 |
| **AI/ML** | OpenAI gpt-4o-mini, FAISS, jhgan/ko-sroberta-multitask |
| **Version Control** | Git, GitHub |
| **Container** | Docker, Docker Compose |

#### 2.2 마이크로서비스 구성

| 서비스명 | 포트 | 역할 |
|----------|------|------|
| Chatbot Server | 8000 | 메인 API 게이트웨이, 사용자 인증 |
| Category Server | 8001 | 의료 카테고리 분류 AI |
| Clinic Server | 8002 | 병원 정보 관리 |
| Drug Server | 8003 | 의약품 정보 서비스 |
| Emergency Support Server | 8004 | 응급의료 지원 |
| Internal External Server | 8005 | 내외부 통신 중계 |

### 3. 프로젝트 주요 특징

#### 3.1 기술적 특징

1. **마이크로서비스 아키텍처**
   - 6개 독립 서비스로 구성된 분산 시스템
   - 서비스별 독립 배포 및 스케일링 가능
   - FastAPI 기반 비동기 처리로 고성능 구현

2. **2단계 LLM 처리 파이프라인**
   - Category Server: 의료 도메인 분류 (1차)
   - Chatbot Server: 도메인별 특화 응답 생성 (2차)
   - 정확도 향상 및 응답 시간 최적화

3. **RAG (Retrieval-Augmented Generation)**
   - FAISS 벡터 DB로 의료 정보 검색
   - jhgan/ko-sroberta-multitask 한국어 임베딩
   - 실시간 의료 정보 업데이트 지원

4. **Template Method Pattern**
   - BaseTemplate 추상 클래스 기반 설계
   - 도메인별 특화 로직 쉽게 추가 가능
   - 코드 재사용성 및 유지보수성 극대화

#### 3.2 성과 및 효과

- **응답 시간**: 평균 1.2초 내 AI 응답 생성
- **동시 처리**: 1,000+ 동시 사용자 처리 가능
- **정확도**: RAG 적용으로 90%+ 응답 정확도
- **확장성**: 새 의료 도메인 30분 내 추가 가능

---

## Ⅱ. 기술 요약 및 UML

### 1. 시스템 아키텍처

```
┌─────────────────────────────────────────────────────────┐
│                     React Frontend                       │
│                    (Port: 3000)                         │
└────────────────────┬────────────────────────────────────┘
                     │ HTTPS/WSS
┌────────────────────▼────────────────────────────────────┐
│               API Gateway (Chatbot Server)              │
│                    Port: 8000                           │
│          - Authentication (JWT)                         │
│          - Request Routing                              │
│          - Template Management                          │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┼────────────┬──────────┬──────────┐
        │            │            │          │          │
┌───────▼──────┐ ┌──▼────────┐ ┌─▼──────┐ ┌▼──────┐ ┌─▼──────┐
│  Category    │ │  Clinic   │ │  Drug  │ │Emergency│ │Internal│
│   Server     │ │  Server   │ │ Server │ │ Support │ │External│
│  Port:8001   │ │Port:8002  │ │Port:8003│ │Port:8004│ │Port:8005│
└──────────────┘ └───────────┘ └────────┘ └─────────┘ └────────┘
        │                │           │          │           │
┌───────▼────────────────▼───────────▼──────────▼───────────▼────┐
│                        Data Layer                               │
│  ┌─────────┐  ┌──────────────┐  ┌─────────┐  ┌──────────┐    │
│  │  MySQL  │  │  Firestore   │  │  Redis  │  │  FAISS   │    │
│  │ (Main)  │  │  (NoSQL)     │  │ (Cache) │  │ (Vector) │    │
│  └─────────┘  └──────────────┘  └─────────┘  └──────────┘    │
└──────────────────────────────────────────────────────────────┘
```

### 2. 핵심 기능 다이어그램

#### 2.1 LLM 처리 시퀀스 다이어그램

```
User -> Frontend: 의료 질문 입력
Frontend -> Chatbot Server: POST /chatbot/send
Chatbot Server -> Category Server: 카테고리 분류 요청
Category Server -> LLM(gpt-4o-mini): 도메인 분석
Category Server --> Chatbot Server: 분류 결과
Chatbot Server -> Redis: 대화 컨텍스트 조회
Chatbot Server -> FAISS: 관련 의료 정보 검색
Chatbot Server -> LLM(gpt-4o-mini): 최종 응답 생성
Chatbot Server -> Redis: 대화 기록 저장
Chatbot Server --> Frontend: 응답 전송
Frontend --> User: AI 응답 표시
```

#### 2.2 Template 생명주기

```python
# Template 초기화 흐름
Application Start
    ├── TemplateContext.add_template(AccountTemplate)
    ├── TemplateContext.add_template(ChatbotTemplate)
    ├── TemplateContext.add_template(CategoryTemplate)
    ├── TemplateContext.add_template(ClinicTemplate)
    ├── TemplateContext.add_template(DrugTemplate)
    └── TemplateContext.add_template(EmergencyTemplate)
         └── 각 Template.init_template()
              ├── DB Connection 초기화
              ├── Cache 초기화
              └── LLM Chain 초기화
```

### 3. 클래스 다이어그램

#### 3.1 Template 구조

```
<<abstract>>
BaseTemplate
├── + init_template(): bool
├── + process_request(data: dict): dict
├── + handle_client_lifecycle(event: str, data: dict): bool
├── # validate_input(data: dict): bool
└── # format_response(data: dict): dict
     │
     ├── AccountTemplateImpl
     │   ├── - jwt_handler: JWTHandler
     │   └── - user_repository: UserRepository
     │
     ├── ChatbotTemplateImpl
     │   ├── - llm_chain: LangChainWrapper
     │   ├── - context_manager: ContextManager
     │   └── - vector_store: FAISSVectorStore
     │
     ├── CategoryTemplateImpl
     │   ├── - classifier: DomainClassifier
     │   └── - category_map: dict
     │
     ├── ClinicTemplateImpl
     │   ├── - clinic_db: ClinicDatabase
     │   └── - location_service: LocationService
     │
     ├── DrugTemplateImpl
     │   ├── - drug_db: DrugDatabase
     │   └── - interaction_checker: DrugInteractionChecker
     │
     └── EmergencyTemplateImpl
         ├── - emergency_chain: EmergencyLangChain
         └── - priority_queue: PriorityQueue
```

#### 3.2 Database Layer

```
MySQLPool
├── - pool: aiomysql.Pool
├── + init(host, port, user, password, db)
├── + call_procedure(proc_name, params): list
└── + execute(query, params): any

RedisCache
├── - client: redis.asyncio.Redis
├── + get_session(session_id): dict
├── + set_session(session_id, data, expire)
├── + get_chat_history(user_id): list
└── + append_chat_history(user_id, message)

FirestoreDB
├── - client: firestore.AsyncClient
├── + get_document(collection, doc_id): dict
├── + set_document(collection, doc_id, data)
└── + query_documents(collection, filters): list
```

---

## Ⅲ. 별첨 (기술 구현 상세)

### 1. FastAPI 마이크로서비스 구현

#### 1.1 메인 서버 구조 (chatbot_server/main.py)

```python
from fastapi import FastAPI
from contextlib import asynccontextmanager
from template.base import TemplateContext, TemplateType
from service.db import MySQLPool
from service.cache import init_cache, CacheConfig
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    """애플리케이션 생명주기 관리"""
    
    # 1. Template 시스템 초기화
    TemplateContext.add_template(TemplateType.ACCOUNT, AccountTemplateImpl())
    TemplateContext.add_template(TemplateType.CHATBOT, ChatbotTemplateImpl())
    
    # 2. 데이터베이스 풀 초기화
    app.state.globaldb = MySQLPool()
    await app.state.globaldb.init(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        db=os.getenv("DB_NAME", "medichain_global")
    )
    
    # 3. Redis 캐시 초기화
    cache_config = CacheConfig(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=int(os.getenv("REDIS_PORT", 6379)),
        session_expire_time=int(os.getenv("REDIS_SESSION_EXPIRE", 3600))
    )
    init_cache(cache_config)
    
    yield  # 서버 실행
    
    # 종료 시 정리
    await app.state.globaldb.close()

app = FastAPI(title="Medical AI Chatbot", lifespan=lifespan)
```

#### 1.2 비동기 요청 처리

```python
@app.post("/chatbot/send")
async def send_message(request: ChatRequest, db=Depends(get_db)):
    """비동기 메시지 처리 엔드포인트"""
    
    # 1. 카테고리 분류 (비동기)
    category = await classify_category(request.message)
    
    # 2. 병렬 처리로 성능 최적화
    context_task = get_chat_context(request.user_id)
    vectors_task = search_vectors(request.message)
    
    context, vectors = await asyncio.gather(context_task, vectors_task)
    
    # 3. LLM 응답 생성
    response = await generate_response(
        message=request.message,
        category=category,
        context=context,
        vectors=vectors
    )
    
    # 4. 결과 저장 (백그라운드)
    asyncio.create_task(save_chat_history(request.user_id, request.message, response))
    
    return {"response": response}
```

### 2. LLM/RAG 통합 시스템

#### 2.1 2단계 LLM 처리 (chatbot_template_impl.py)

```python
class ChatbotTemplateImpl(BaseTemplate):
    async def process_request(self, request_data: dict) -> dict:
        """2단계 LLM 처리 파이프라인"""
        
        message = request_data.get("message")
        user_id = request_data.get("user_id")
        
        # Stage 1: 카테고리 서버로 도메인 분류
        async with httpx.AsyncClient() as client:
            category_response = await client.post(
                "http://localhost:8001/categorize",
                json={"message": message}
            )
            category = category_response.json()["category"]
        
        # Stage 2: 카테고리별 특화 처리
        if category == "emergency":
            handler = self.emergency_handler
        elif category == "drug":
            handler = self.drug_handler
        elif category == "clinic":
            handler = self.clinic_handler
        else:
            handler = self.general_handler
        
        # LLM 체인 실행 (gpt-4o-mini)
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.2,
            max_tokens=1000
        )
        
        response = await handler.process_with_llm(llm, message, user_id)
        
        return self.format_response({"message": response})
```

#### 2.2 RAG 구현 (emergency_support_lang_chain.py)

```python
from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter

class EmergencySupportLangChain:
    def __init__(self):
        # 한국어 특화 임베딩 모델
        self.embeddings = SentenceTransformer('jhgan/ko-sroberta-multitask')
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        self.vector_store = None
        
    async def init(self):
        """벡터 스토어 초기화"""
        # 응급의료 문서 로드
        documents = await self.load_emergency_documents()
        
        # 텍스트 분할
        splits = self.text_splitter.split_documents(documents)
        
        # FAISS 벡터 스토어 생성
        self.vector_store = FAISS.from_documents(
            splits, 
            self.embeddings
        )
        
    async def generate_response(self, query: str) -> str:
        """RAG 기반 응답 생성"""
        
        # 1. 관련 문서 검색 (k=5)
        relevant_docs = self.vector_store.similarity_search(query, k=5)
        
        # 2. 컨텍스트 구성
        context = "\n".join([doc.page_content for doc in relevant_docs])
        
        # 3. 프롬프트 구성
        prompt = f"""당신은 응급의료 전문가입니다.
        
        관련 정보:
        {context}
        
        질문: {query}
        
        위 정보를 바탕으로 정확하고 도움이 되는 답변을 제공하세요."""
        
        # 4. LLM 호출 (gpt-4o-mini)
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)
        response = await llm.ainvoke(prompt)
        
        return response.content
```

### 3. Template Pattern 구현

#### 3.1 Base Template (base_template.py)

```python
from abc import ABC, abstractmethod

class BaseTemplate(ABC):
    """모든 도메인 템플릿의 기본 클래스"""
    
    @abstractmethod
    async def init_template(self) -> bool:
        """템플릿 초기화 - 각 도메인별 구현 필요"""
        pass
    
    @abstractmethod
    async def process_request(self, request_data: dict) -> dict:
        """요청 처리 - 각 도메인별 핵심 로직"""
        pass
    
    @abstractmethod
    async def handle_client_lifecycle(self, event: str, client_data: dict) -> bool:
        """클라이언트 생명주기 이벤트 처리"""
        pass
    
    def validate_input(self, data: dict) -> bool:
        """공통 입력 검증 로직"""
        required_fields = self.get_required_fields()
        return all(field in data for field in required_fields)
    
    def format_response(self, data: dict) -> dict:
        """표준 응답 형식"""
        return {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "data": data
        }
```

#### 3.2 도메인별 구현 예시 (clinic_template_impl.py)

```python
class ClinicTemplateImpl(BaseTemplate):
    """병원 정보 도메인 템플릿"""
    
    async def init_template(self) -> bool:
        """병원 데이터 및 위치 서비스 초기화"""
        self.clinic_db = ClinicDatabase()
        await self.clinic_db.connect()
        
        self.location_service = LocationService()
        await self.location_service.init()
        
        return True
    
    async def process_request(self, request_data: dict) -> dict:
        """병원 검색 및 추천 처리"""
        location = request_data.get("location")
        specialty = request_data.get("specialty")
        
        # 근처 병원 검색
        nearby_clinics = await self.clinic_db.find_nearby(
            location=location,
            radius=5000,  # 5km
            specialty=specialty
        )
        
        # 평점 및 대기시간 기준 정렬
        sorted_clinics = self.sort_by_score(nearby_clinics)
        
        return self.format_response({
            "clinics": sorted_clinics[:10],
            "total": len(nearby_clinics)
        })
    
    async def handle_client_lifecycle(self, event: str, client_data: dict) -> bool:
        """클라이언트 이벤트 처리"""
        if event == "connect":
            # 사용자 위치 정보 캐싱
            await self.cache_user_location(client_data)
        elif event == "disconnect":
            # 임시 데이터 정리
            await self.cleanup_temp_data(client_data)
        
        return True
```

---

**프로젝트 GitHub**: https://github.com/SKN12-4th-5TEAM

**팀원 코멘트**
- 권성호: "마이크로서비스 아키텍처 설계를 주도하며 확장성 있는 시스템을 구축했습니다."
- 남의헌: "LLM 통합과 RAG 시스템 구현으로 AI 정확도를 크게 향상시켰습니다."
- 손현성: "프론트엔드와 백엔드 통합을 담당하며 사용자 경험을 최적화했습니다."
- 이준배: "데이터베이스 설계와 캐싱 전략으로 성능을 극대화했습니다."
- 이준석: "Template Pattern 적용으로 새로운 도메인 추가가 매우 용이해졌습니다."

---

작성일: 2024년 12월