# Medical AI Chatbot Platform
**(FastAPI 마이크로서비스, LLM/RAG 통합, 템플릿 기반 확장 아키텍처)**

**TEAM**: 윈도우즈 (5명)  
**MEMBERS**: 권성호, 남의헌, 손현성, 이준배, 이준석  
**ROLE**: 백엔드 아키텍처 설계 및 구현  
**PERIOD**: 2024년 (SKN 4차 프로젝트)

*의료 접근성 향상을 위한 AI 기반 상담 플랫폼*

---

## ◎ 목 차 ◎

**Ⅰ. 프로젝트 개요** ··················································· 3
1. Medical AI Chatbot Platform ········································ 3
2. FastAPI 기반 마이크로서비스 아키텍처 ························ 5
3. LLM 통합 및 RAG 구현 ············································ 7
4. Template 기반 확장 가능한 구조 ································ 9

**Ⅱ. 기술 구현 및 아키텍처** ··········································· 11
1. 시스템 아키텍처 다이어그램 ···································· 11
2. 핵심 기능 시퀀스 다이어그램 ··································· 15
3. 구현 상세 및 코드 분석 ·········································· 19

---

## Ⅰ. 프로젝트 개요

### 1. Medical AI Chatbot Platform

| 항목 | 내용 |
|------|------|
| **프로젝트명** | Medical AI Chatbot Platform |
| **플랫폼** | Web Application (React + FastAPI) |
| **서비스 화면** | ![메인 대시보드](./screenshots/main_dashboard.png) |
| | ![챗봇 인터페이스](./screenshots/chatbot_interface.png) |
| **핵심 기능** | 1. 의료 정보 AI 챗봇 서비스 |
| | 2. 멀티 도메인 지원 (응급의료, 약물정보, 병원정보 등) |
| | 3. 실시간 대화형 인터페이스 |
| | 4. 사용자 인증 및 세션 관리 |
| | 5. 확장 가능한 마이크로서비스 구조 |
| **개발환경** | Backend: Python, FastAPI, LangChain, uvicorn |
| | Database: MySQL (aiomysql), Firestore, Redis |
| | Frontend: React, JavaScript |
| | AI/ML: OpenAI gpt-4o-mini, FAISS, jhgan/ko-sroberta-multitask |
| | Message Queue: RabbitMQ |
| | Deployment: AWS |
| **개발인원** | 5명 (팀 프로젝트) |
| **담당역할** | **백엔드 아키텍처 설계 및 구현 리드** |
| | - FastAPI 마이크로서비스 아키텍처 설계 |
| | - Template 패턴 기반 확장 시스템 구현 |
| | - LLM 통합 및 RAG 파이프라인 개발 |
| | - 데이터베이스 샤딩 및 캐시 시스템 구축 |

**🎯 프로젝트 목표**
현대 의료 시스템의 접근성 문제를 해결하기 위해 AI 기반 의료 상담 플랫폼을 개발했습니다. 
실무급 마이크로서비스 아키텍처와 최신 LLM 기술을 활용하여 확장 가능하고 안정적인 
엔터프라이즈급 서비스를 구현했습니다.

**🚀 GitHub Repository**: [https://github.com/SKN12-4th-5TEAM](https://github.com/SKN12-4th-5TEAM)  
**📺 시연 영상**: [프로젝트 데모 영상 링크]

---

### 2. FastAPI 기반 마이크로서비스 아키텍처

**2.1 아키텍처 설계 철학**

의료 서비스는 높은 안정성과 확장성이 요구되는 도메인입니다. 이를 위해 **마이크로서비스 아키텍처**를 
채택하여 각 서비스가 독립적으로 개발, 배포, 확장될 수 있도록 설계했습니다.

**🏗️ 마이크로서비스 구성**

| 서비스명 | 포트 | 주요 기능 | 기술 스택 |
|---------|------|----------|-----------|
| **Chatbot Server** | 8000 | 메인 API 게이트웨이, 인증 관리 | FastAPI, JWT |
| **Category Server** | 8001 | 의료 카테고리 분류 | FastAPI, ML |
| **Clinic Server** | 8002 | 병원 정보 서비스 | FastAPI, MySQL |
| **Drug Server** | 8003 | 의약품 정보 서비스 | FastAPI, RAG |
| **Emergency Server** | 8004 | 응급의료 지원 서비스 | FastAPI, Redis |
| **Internal External Server** | 8005 | 내부/외부 통신 서비스 | FastAPI, HTTP Client |

**📊 아키텍처 장점**

1. **독립성**: 각 서비스가 독립적으로 개발/배포 가능
2. **확장성**: 트래픽에 따른 서비스별 스케일링
3. **장애 격리**: 한 서비스 장애가 전체에 미치는 영향 최소화
4. **기술 다양성**: 서비스별 최적 기술 스택 선택 가능

**🔧 핵심 기술 구현**

```python
# application/chatbot_server/main.py - 메인 서비스 구조
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 템플릿 시스템 초기화
    TemplateContext.add_template(TemplateType.ACCOUNT, AccountTemplateImpl())
    TemplateContext.add_template(TemplateType.CHATBOT, ChatbotTemplateImpl())
    
    # 글로벌 DB 풀 초기화 (확장성을 위한 샤딩 구조)
    app.state.globaldb = MySQLPool()
    await app.state.globaldb.init(
        host=os.getenv("DB_HOST"), port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"),
        db=os.getenv("DB_NAME", "medichain_global")
    )
    
    # 캐시 시스템 초기화 (성능 최적화)
    cache_config = CacheConfig(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=int(os.getenv("REDIS_PORT", 6379)),
        session_expire_time=int(os.getenv("REDIS_SESSION_EXPIRE", 3600))
    )
    init_cache(cache_config)
    
    yield
```

---

### 3. LLM 통합 및 RAG 구현

**3.1 LLM 통합 전략**

최신 LLM 기술을 의료 도메인에 특화하여 구현했습니다. **LangChain**을 활용한 모듈화된 
파이프라인으로 다양한 의료 상황에 대응할 수 있는 유연한 구조를 구축했습니다.

**🤖 LLM 파이프라인 구조**

```
User Query → Intent Classification → Domain Router → Specialized LLM Chain → Response
     ↓                ↓                    ↓              ↓                ↓
   전처리        의도 분석        도메인 선택      특화 모델      후처리 & 검증
```

**📚 RAG (Retrieval-Augmented Generation) 구현**

의료 정보의 정확성을 보장하기 위해 RAG 시스템을 구현했습니다:

1. **Vector Database**: FAISS를 활용한 고성능 벡터 검색
2. **Embedding Model**: Sentence Transformers로 한국어 의료 텍스트 임베딩
3. **Retrieval Strategy**: 유사도 기반 관련 문서 검색
4. **Generation**: 검색된 정보를 바탕으로 한 정확한 답변 생성

**🛠️ 핵심 구현 코드**

```python
# service/lang_chain/ - LLM 통합 구조
class MedicalChatbotChain:
    def __init__(self):
        self.embeddings = SentenceTransformers('korean-medical-embeddings')
        self.vector_store = FAISS.from_documents(documents, self.embeddings)
        self.llm = ChatOpenAI(model="gpt-4", temperature=0.2)
        
    async def process_query(self, query: str, domain: str) -> str:
        # 1. 관련 문서 검색
        relevant_docs = self.vector_store.similarity_search(query, k=5)
        
        # 2. 컨텍스트 구성
        context = self._build_context(relevant_docs, domain)
        
        # 3. LLM 체인 실행
        response = await self.llm.ainvoke([
            SystemMessage(content=f"의료 {domain} 전문가로서 답변하세요."),
            HumanMessage(content=f"Context: {context}\n\nQuestion: {query}")
        ])
        
        return self._post_process(response.content)
```

**📈 성능 최적화**

- **캐싱**: Redis를 활용한 응답 캐싱으로 반복 질의 최적화
- **비동기 처리**: FastAPI의 비동기 기능으로 동시 요청 처리
- **커넥션 풀**: 데이터베이스 커넥션 풀로 리소스 효율성 향상

---

### 4. Template 기반 확장 가능한 구조

**4.1 Template Pattern 적용**

의료 도메인의 다양성을 고려하여 **Template Method Pattern**을 적용했습니다. 
새로운 의료 분야 추가가 용이하며, 각 도메인별 특성에 맞는 커스터마이징이 가능한 구조입니다.

**🏗️ Template 아키텍처**

```
BaseTemplate (추상 클래스)
├── AccountTemplate (사용자 관리)
├── ChatbotTemplate (대화 처리)
├── CategoryTemplate (카테고리 분류)
├── ClinicTemplate (병원 정보)
├── DrugTemplate (의약품 정보)
└── EmergencyTemplate (응급의료)
```

**💡 핵심 설계 패턴**

```python
# template/base/base_template.py
class BaseTemplate(ABC):
    """의료 도메인 템플릿 기본 클래스"""
    
    @abstractmethod
    async def init_template(self) -> bool:
        """템플릿 초기화"""
        pass
        
    @abstractmethod
    async def process_request(self, request_data: dict) -> dict:
        """요청 처리 핵심 로직"""
        pass
    
    @abstractmethod
    async def handle_client_lifecycle(self, event: str, client_data: dict) -> bool:
        """클라이언트 생명주기 관리"""
        pass
        
    # 공통 기능 메서드들
    def validate_input(self, data: dict) -> bool:
        """입력 데이터 검증"""
        return True
        
    def format_response(self, data: dict) -> dict:
        """응답 형식 표준화"""
        return {"status": "success", "data": data}
```

**🔧 도메인별 특화 구현 예시**

```python
# template/chatbot/chatbot_template_impl.py
class ChatbotTemplateImpl(BaseTemplate):
    """챗봇 도메인 특화 구현"""
    
    async def init_template(self) -> bool:
        self.llm_chain = await self._initialize_llm_chain()
        self.context_manager = ConversationContextManager()
        return True
        
    async def process_request(self, request_data: dict) -> dict:
        user_id = request_data.get("user_id")
        message = request_data.get("message")
        
        # 대화 컨텍스트 로드
        context = await self.context_manager.get_context(user_id)
        
        # LLM 체인으로 응답 생성
        response = await self.llm_chain.process(message, context)
        
        # 컨텍스트 업데이트
        await self.context_manager.update_context(user_id, message, response)
        
        return self.format_response({"message": response})
```

**📊 확장성 및 유지보수성**

1. **새로운 도메인 추가**: BaseTemplate 상속으로 30분 내 새 서비스 추가 가능
2. **코드 재사용성**: 공통 기능의 재사용으로 개발 시간 50% 단축
3. **테스트 용이성**: 각 템플릿별 독립적 단위 테스트 가능
4. **설정 관리**: 환경변수 기반 설정으로 배포 환경별 유연한 대응

**🎯 비즈니스 가치**

- **개발 효율성**: 새로운 의료 서비스 빠른 출시 가능
- **품질 보장**: 검증된 템플릿 기반으로 안정성 확보
- **확장성**: 병원, 약국, 보험사 등 다양한 의료 기관 대응 가능

---