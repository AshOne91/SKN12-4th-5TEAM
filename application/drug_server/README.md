# Drug Server

## 📌 개요
Drug Server는 **약품 정보 전용 마이크로서비스**입니다. Vector_store 클래스를 활용한 RAG 시스템을 통해 약물 관련 질문에 대한 전문적인 응답을 제공합니다.

## 🚀 실행 방법
```bash
python application/drug_server/main.py
```

## 🏗️ 구조
```
application/drug_server/
├── main.py              # FastAPI 서버 엔트리포인트
└── routers/
    ├── __init__.py
    └── drug.py          # 약품 정보 API 라우터
```

## ⚙️ 서버 설정

### 템플릿 초기화
```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    drug_template_instance = DrugTemplateImpl()
    drug_template_instance.init(config=None)
    # TemplateType을 DRUG로 정확하게 지정합니다.
    TemplateContext.add_template(TemplateType.DRUG, drug_template_instance)
    yield
```

**특징**:
- `DrugTemplateImpl()` 생성자에서 `Vector_store` 인스턴스 초기화
- 추가로 `init(config=None)` 메서드 호출 (프레임워크 호환성)
- `TemplateType.DRUG`로 명시적 타입 지정

### FastAPI 애플리케이션
```python
app = FastAPI(lifespan=lifespan)
app.include_router(drug.router, prefix="/drug", tags=["drug"])
```

## 🔗 API 엔드포인트

### 루트 엔드포인트
- **GET** `/` - 서버 상태 확인
- **응답**: `{"message": "Drug Server is running"}`

### 약품 정보 API
- **접두사**: `/drug`
- **태그**: `["drug"]`
- **라우터**: `drug.router`

**주석 처리된 대안**:
```python
# app.include_router(drug.router, prefix="/drug_server", tags=["drug"])
```

## 💊 RAG 시스템 구성

DrugTemplateImpl이 사용하는 Vector_store 구성 요소:
- **FAISS 인덱스**: 약품 정보 벡터 검색
- **텍스트 청크**: 약품 관련 문서 조각들
- **임베딩 모델**: 질문 벡터화
- **LangChain RAG 체인**: OpenAI와 통합된 응답 생성

## 🗄️ 환경변수

DrugTemplateImpl에서 사용되는 환경변수들:
- `OPENAI_API_KEY` - OpenAI API 키
- `DRUG_VECTORDB_INDEX` - FAISS 인덱스 파일 경로
- `DRUG_VECTORDB_TXT` - 약품 정보 텍스트 파일 경로

## 💡 실제 코드 특징

1. **클래스 기반 RAG**: `Vector_store` 클래스로 캡슐화된 RAG 시스템
2. **이중 초기화**: 생성자(`__init__`)와 메서드(`init`) 모두 호출
3. **타입 명시**: `TemplateType.DRUG` 주석으로 명확한 타입 지정 의도 표현
4. **단일 책임**: 약품 정보만 담당하는 전용 서비스
5. **독립 실행**: 다른 서비스와 독립적으로 동작

## 📋 약품 정보 도메인

이 서버가 다루는 약품 관련 정보:
- 처방약 정보 및 효능
- 복용법 및 주의사항
- 약물 상호작용
- 부작용 및 금기사항
- 약물 식별 및 검색

이 서버는 **약품 정보 전문가**로서 안전하고 정확한 약물 정보를 제공하는 **전용 RAG 서비스**입니다.