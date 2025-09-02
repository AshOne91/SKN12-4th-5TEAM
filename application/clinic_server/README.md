# Clinic Server

## 📌 개요
Clinic Server는 **병원 및 의료 정보 전용 마이크로서비스**입니다. FAISS 벡터 검색과 GPT-4o를 활용한 RAG 시스템을 통해 병원/의료진 관련 질문에 대한 전문적인 응답을 제공합니다.

## 🚀 실행 방법
```bash
python application/clinic_server/main.py
```

## 🏗️ 구조
```
application/clinic_server/
├── main.py              # FastAPI 서버 엔트리포인트
└── routers/
    ├── __init__.py
    └── clinic.py        # 병원 정보 API 라우터
```

## ⚙️ 서버 설정

### 명시적 템플릿 초기화
```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    clinic_template_instance = ClinicTemplateImpl()
    clinic_template_instance.init(config=None)  # 명시적 init() 호출
    TemplateContext.add_template(TemplateType.CLINIC, clinic_template_instance)
    yield
```

**특징**:
- 다른 서버와 달리 **명시적으로 `init()` 메서드 호출**
- 템플릿 인스턴스 생성 후 수동으로 초기화
- RAG 리소스(FAISS, 임베딩 모델 등) 사전 로드

### FastAPI 애플리케이션
```python
app = FastAPI(lifespan=lifespan)
app.include_router(clinic.router, prefix="/clinic", tags=["clinic"])
```

## 🔗 API 엔드포인트

### 루트 엔드포인트
- **GET** `/` - 서버 상태 확인
- **응답**: `{"message": "Clinic Server is running"}`

### 병원 정보 API
- **접두사**: `/clinic`
- **태그**: `["clinic"]`
- **라우터**: `clinic.router`

**주석 처리된 대안**:
```python
# app.include_router(clinic.router, prefix="/clinic_server", tags=["clinic"])
```

## 🗄️ 환경변수 로드
```python
load_dotenv()
```

ClinicTemplateImpl에서 사용되는 환경변수들:
- `CLINIC_VECTORDB_BASE` - FAISS 인덱스와 문서 ID 파일 기본 경로
- `CLINIC_VECTORDB_DOCS` - 처리된 문서 파일들 경로
- `OPENAI_API_KEY` - OpenAI API 키

## 💡 실제 코드 특징

1. **명시적 초기화**: 유일하게 `init(config=None)` 메서드를 직접 호출
2. **RAG 전용**: 병원/의료진 정보 RAG 시스템에 특화
3. **리소스 집약적**: FAISS 인덱스, 임베딩 모델, GPT-4o 등 무거운 리소스 사용
4. **독립 실행**: 다른 서비스와 독립적으로 동작
5. **환경변수 의존**: 벡터 DB 경로 설정을 환경변수로 관리

## 🧠 RAG 시스템 구성

Clinic Server가 초기화 시 로드하는 RAG 컴포넌트들:
- FAISS 벡터 인덱스 (검색)
- SentenceTransformer 임베딩 모델 (질문 벡터화)
- 문서 ID 매핑 (검색 결과 → 문서 매칭)
- 키워드 인덱스 (fallback 검색)
- OpenAI GPT-4o 클라이언트 (응답 생성)

이 서버는 **병원 정보 전문가**로서 의료 기관, 의료진, 진료과목 등에 대한 정확한 정보를 제공하는 **전용 RAG 서비스**입니다.