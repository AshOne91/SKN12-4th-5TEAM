# Internal External Server

## 📌 개요
Internal External Server는 **내과/외과 구분 전용 마이크로서비스**입니다. Emergency Support와 동일한 함수 기반 RAG 모듈을 활용하여 내과/외과 질문에 대한 전문적인 응답을 제공합니다.

## 🚀 실행 방법
```bash
python application/internal_external_server/main.py
```

## 🏗️ 구조
```
application/internal_external_server/
├── main.py              # FastAPI 서버 엔트리포인트
└── routers/
    ├── __init__.py
    └── internal_external.py  # 내과/외과 API 라우터
```

## ⚙️ 서버 설정

### 템플릿 초기화
```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    internal_external_template_instance = InternalExternalTemplateImpl()
    # config 인자는 현재 init 메서드에서 사용되지 않으므로 None을 전달합니다.
    internal_external_template_instance.init(config=None)
    TemplateContext.add_template(TemplateType.INTERNAL_EXTERNAL, internal_external_template_instance)
    yield
```

**특징**:
- `InternalExternalTemplateImpl`은 BaseTemplate을 상속하지 않음
- `__init__()`에서 RAG 리소스 직접 초기화 (Emergency Support와 다름)
- 추가로 `init(config=None)` 메서드도 호출

### FastAPI 애플리케이션
```python
app = FastAPI(lifespan=lifespan)
app.include_router(internal_external.router, prefix="/internal_external", tags=["internal-external"])
```

## 🔗 API 엔드포인트

### 루트 엔드포인트
- **GET** `/` - 서버 상태 확인
- **응답**: `{"message": "Internal & External Server is running"}`

### 내과/외과 구분 API
- **접두사**: `/internal_external`
- **태그**: `["internal-external"]`
- **라우터**: `internal_external.router`

**주석 처리된 대안**:
```python
# app.include_router(internal_external.router, prefix="/internal_external_server", tags=["internal-external"])
```

## ⚖️ 내과/외과 RAG 시스템

InternalExternalTemplateImpl의 RAG 구성 요소 (Emergency Support와 동일):
- **임베딩 모델**: `load_embedding_model()` - 한국어 특화 임베딩
- **FAISS 인덱스**: `load_faiss_index()` - 내과/외과 벡터 검색
- **문서 청크**: `load_chunks()` - 내과/외과 구분 가이드 텍스트
- **RAG 체인**: `build_rag_chain()` - LangChain + OpenAI 통합

## 🗄️ 환경변수

InternalExternalTemplateImpl에서 사용되는 환경변수들:
- `OPENAI_API_KEY` - OpenAI API 키
- `INTERNAL_EXTERNAL_VECTORDB_INDEX` - FAISS 인덱스 파일 경로
- `INTERNAL_EXTERNAL_VECTORDB_TXT` - 내과/외과 텍스트 파일 경로

## 🏥 내과/외과 도메인

이 서버가 다루는 내과/외과 구분 정보:
- **내과 질환**: 내부 장기 질병, 만성질환, 내과적 치료
- **외과 질환**: 수술적 치료 대상, 외상, 종양 등
- **구분 기준**: 증상에 따른 적절한 진료과 추천
- **치료 방향**: 보존적 치료 vs 수술적 치료 판단

## 💡 실제 코드 특징

1. **코드 재사용**: Emergency Support와 동일한 RAG 함수 사용
2. **초기화 방식 차이**: `__init__()`에서 직접 초기화 (Emergency와 다름)
3. **상속 구조 차이**: BaseTemplate을 상속하지 않는 독립적 구현
4. **주석된 코드**: 개발 과정에서 Emergency Support를 참고한 흔적
5. **단순한 구조**: CORS 미들웨어 없는 최소한의 설정

**주석된 Emergency Support 흔적**:
```python
# TemplateContext.add_template(TemplateType.EMERGENCY_SUPPORT, EmergencySupportTemplateImpl())
```

**파일 끝부분의 구분선**:
```python
# ------------------------------------------------------------
```

## 🧬 코드 동일성

이 서버가 사용하는 `service/lang_chain/internal_external_lang_chain.py`는 `emergency_support_lang_chain.py`와 완전히 동일한 코드입니다. 차이점은 다음과 같습니다:

| 구분 | Emergency Support | Internal External |
|------|------------------|-------------------|
| **템플릿 상속** | EmergencySupportTemplate 상속 | BaseTemplate 미상속 |
| **초기화 시점** | `init()` 메서드에서 | `__init__()` 생성자에서 |
| **CORS 설정** | React 연동 CORS 설정 | CORS 미설정 |
| **벡터 데이터** | 응급 의료 데이터 | 내과/외과 구분 데이터 |

이 서버는 **내과/외과 전문 상담사**로서 증상과 질병을 기반으로 적절한 진료과 추천과 치료 방향을 제시하는 **전문 진료과 라우팅 서비스**입니다.