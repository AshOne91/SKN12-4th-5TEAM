# Drug Template Module

## 📌 모듈 개요
Drug 템플릿은 **약품 정보 전문 RAG 시스템**을 구현합니다. `Vector_store` 클래스를 사용하여 약품 관련 질문에 대한 전문적인 응답을 제공합니다.

## 🏗️ 실제 구조

```
template/drug/
├── drug_template_impl.py  # 약품 정보 RAG 로직 구현
└── common/
    └── drug_serialize.py  # 요청/응답 스키마
```

## 🤖 핵심 기능 분석

### 1. DrugTemplateImpl 초기화
```python
class DrugTemplateImpl(DrugTemplate):
    def __init__(self):
        super().__init__()
        print("Initializing Vector_store for DrugTemplate...")
        
        # Vector_store 인스턴스 생성 및 저장
        self.vector_store = Vector_store(
            api_key=OPENAI_API_KEY,
            chunk_path=CHUNK_PATH,
            index_path=INDEX_PATH,
        )
        print("Vector_store for DrugTemplate initialized.")
```

**실제 사용되는 환경변수**:
- `OPENAI_API_KEY` - OpenAI API 키
- `DRUG_VECTORDB_INDEX` - FAISS 인덱스 파일 경로
- `DRUG_VECTORDB_TXT` - 약품 정보 텍스트 파일 경로

### 2. 약품 질의 처리
```python
async def on_drug_ask_req(self, client_session, request: DrugAskRequest) -> DrugAskResponse:
    question = request.question
    # 사전 초기화된 Vector_store 인스턴스 사용
    answer = await self.vector_store.rag_answer(question)
    return DrugAskResponse(answer=answer)
```

**처리 특징**:
- `__init__`에서 생성한 `Vector_store` 인스턴스 재사용
- `rag_answer()` 메서드로 비동기 RAG 처리
- 간단하고 직관적인 질의-응답 구조

## 📊 요청/응답 스키마

### DrugAskRequest
```python
class DrugAskRequest(BaseRequest):
    question: str  # 약품 관련 질문
```

### DrugAskResponse
```python
class DrugAskResponse(BaseResponse):
    answer: str    # RAG 시스템이 생성한 응답
```

## 🔄 처리 플로우

```
사용자 약품 질문
    ↓
DrugTemplateImpl.on_drug_ask_req()
    ↓
Vector_store.rag_answer() (비동기)
    ↓
RAG 응답 반환
```

## 💡 설계 패턴

### 1. 리소스 효율적 초기화
```python
def __init__(self):
    """
    DrugTemplateImpl initializer.
    The Vector_store is loaded once here to manage resources efficiently.
    """
    # Vector_store 인스턴스를 한 번만 생성하고 애플리케이션 생명주기 동안 재사용
    self.vector_store = Vector_store(...)
```

**장점**:
- 메모리 효율성: 벡터 DB와 모델을 한 번만 로드
- 성능 향상: 매 요청마다 초기화 오버헤드 제거
- 리소스 관리: 애플리케이션 생명주기와 연동

### 2. 프레임워크 호환성
```python
def init(self, config):
    """Drug template initializer (for framework compatibility)"""
    # The actual initialization is done in __init__.
    print("Drug template init hook called.")
```

**목적**:
- 기존 프레임워크의 `init()` 호출과 호환
- 실제 초기화는 `__init__`에서 수행

## 🔗 의존성

### 사용하는 모듈
- `service.lang_chain.drug_lang_chain.Vector_store` - 약품 RAG 시스템
- `template.drug.common.drug_serialize` - 요청/응답 모델
- `template.base.template.drug_template.DrugTemplate` - 기본 템플릿

### 사용하는 라이브러리
- `dotenv` - 환경변수 로드
- `os` - 환경변수 접근

## 🖥️ 로깅

**실제 구현된 로그 메시지**:
```python
print("Initializing Vector_store for DrugTemplate...")
print("Vector_store for DrugTemplate initialized.")
print("Drug template init hook called.")
print("Drug data loaded")
print("Drug client created")
print("Drug client updated") 
print("Drug client deleted")
```

## 💭 실제 코드의 특징

1. **단순함**: 복잡한 로직 없이 Vector_store에 위임
2. **효율성**: 리소스를 한 번만 로드하여 메모리와 시간 절약
3. **비동기 지원**: `await`를 통한 non-blocking RAG 처리
4. **프레임워크 호환**: 기존 템플릿 시스템과 완전 호환
5. **명확한 책임**: 약품 정보 질의만 담당

## 🏗️ Vector_store 연동

Drug 템플릿은 실제 RAG 로직을 `service.lang_chain.drug_lang_chain.Vector_store`에 완전히 위임합니다:

- **초기화**: `Vector_store(api_key, chunk_path, index_path)` 생성자 호출
- **질의**: `await vector_store.rag_answer(question)` 메서드 호출
- **응답**: Vector_store가 반환한 답변을 그대로 전달

이는 **관심사의 분리** 원칙을 따른 설계로, 템플릿 레이어는 비즈니스 흐름만 관리하고 실제 AI 처리는 서비스 레이어에 맡깁니다.

이 모듈은 **약품 정보 전문가**로서 의료진과 환자에게 정확한 약물 정보를 제공하는 **전용 RAG 인터페이스**입니다.