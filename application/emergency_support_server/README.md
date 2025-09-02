# Emergency Support Server

## 📌 개요
Emergency Support Server는 **응급 의료 지원 전용 마이크로서비스**입니다. 함수 기반 RAG 모듈을 활용하여 응급 상황 관련 질문에 대한 전문적이고 신속한 응답을 제공합니다.

## 🚀 실행 방법
```bash
python application/emergency_support_server/main.py
```

## 🏗️ 구조
```
application/emergency_support_server/
├── main.py              # FastAPI 서버 엔트리포인트
└── routers/
    ├── __init__.py
    └── emergency_support.py  # 응급 지원 API 라우터
```

## ⚙️ 서버 설정

### 템플릿 초기화
```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    emergency_template_instance = EmergencySupportTemplateImpl()
    # config 인자는 현재 init 메서드에서 사용되지 않으므로 None을 전달합니다.
    emergency_template_instance.init(config=None)
    TemplateContext.add_template(TemplateType.EMERGENCY_SUPPORT, emergency_template_instance)
    yield
```

**특징**:
- `init(config=None)` 메서드에서 RAG 리소스 로드
- 함수 기반 RAG 모듈(`emergency_support_lang_chain`) 활용
- 주석으로 config 사용하지 않음을 명시

### CORS 미들웨어
```python
origins = [
    "http://localhost:3000",  # React 앱 주소
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**특징**: 프론트엔드(React)와의 통신을 위한 특정 도메인 허용

## 🔗 API 엔드포인트

### 루트 엔드포인트
- **GET** `/` - 서버 상태 확인
- **응답**: `{"message": "Emergency & Support Server is running"}`

### 응급 지원 API
- **접두사**: `/emergency-support`
- **태그**: `["emergency-support"]`
- **라우터**: `emergency_support.router`

**주석 처리된 대안**:
```python
# app.include_router(emergency_support.router, prefix="/emergency-support_server", tags=["emergency-support"])
```

## 🚨 응급 의료 RAG 시스템

EmergencySupportTemplateImpl의 RAG 구성 요소:
- **임베딩 모델**: `load_embedding_model()` - 한국어 특화 임베딩
- **FAISS 인덱스**: `load_faiss_index()` - 응급 의료 벡터 검색
- **문서 청크**: `load_chunks()` - 응급 처치 가이드 텍스트
- **RAG 체인**: `build_rag_chain()` - LangChain + OpenAI 통합

## 🗄️ 환경변수

EmergencySupportTemplateImpl에서 사용되는 환경변수들:
- `OPENAI_API_KEY` - OpenAI API 키
- `EMERGENCY_SUPPORT_VECTORDB_INDEX` - FAISS 인덱스 파일 경로
- `EMERGENCY_SUPPORT_VECTORDB_TXT` - 응급 지원 텍스트 파일 경로

## 🚑 응급 의료 도메인

이 서버가 다루는 응급 상황 정보:
- 응급처치 방법 및 절차
- 증상별 응급 대응 요령
- 응급실 방문 기준 및 판단
- 응급 약물 정보 및 사용법
- 생명 위험 상황 판단 가이드

## 💡 실제 코드 특징

1. **함수 기반 RAG**: 클래스가 아닌 함수로 구성된 모듈러 RAG 시스템
2. **CORS 지원**: React 프론트엔드와의 직접 통신 지원
3. **명시적 초기화**: `init()` 메서드에서 모든 RAG 컴포넌트 로드
4. **응급 특화**: 생명과 직결된 응급 상황에 특화된 전문 서비스
5. **주석 상세**: 개발 과정의 의도와 변경사항이 주석으로 기록됨

**주석된 import 구문들**:
```python
# from fastapi_base_server.application.emergency_support_server.routers import emergency_support
# from . import chatbot
# TemplateContext.add_template(TemplateType.EMERGENCY_SUPPORT, EmergencySupportTemplateImpl())
```

이 서버는 **응급 의료 전문가**로서 생명과 직결된 응급 상황에서 정확하고 신속한 의료 정보를 제공하는 **생명 구조 RAG 서비스**입니다.