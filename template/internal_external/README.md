# Internal External Template Module

## 📌 모듈 개요
Internal External 템플릿은 **내과/외과 구분 RAG 시스템**을 구현합니다. Emergency Support와 동일한 함수 기반 RAG 모듈을 사용하여 내과/외과 질문에 대한 전문적인 응답을 제공합니다.

## 🏗️ 실제 구조

```
template/internal_external/
├── internal_external_template_impl.py  # 내과/외과 RAG 로직 구현
└── common/
    └── internal_external_serialize.py  # 요청/응답 스키마
```

## 🤖 핵심 기능 분석

### 1. InternalExternalTemplateImpl 초기화
```python
class InternalExternalTemplateImpl:
    def __init__(self):
        self.embed_model = load_embedding_model()
        self.index = load_faiss_index(INDEX_PATH)
        self.chunks = load_chunks(CHUNK_PATH)
        self.rag_chain = build_rag_chain(OPENAI_API_KEY)
```

**주목할 점**:
- **BaseTemplate 미상속**: 다른 템플릿과 달리 기본 템플릿을 상속하지 않음
- **__init__ 초기화**: Emergency Support와 달리 생성자에서 RAG 리소스 로드
- **commented import**: `# from template.base.template.internal_external_template import InternalExternalTemplate` 주석 처리됨

**실제 사용되는 환경변수**:
- `OPENAI_API_KEY` - OpenAI API 키
- `INTERNAL_EXTERNAL_VECTORDB_INDEX` - FAISS 인덱스 파일 경로  
- `INTERNAL_EXTERNAL_VECTORDB_TXT` - 내과/외과 텍스트 파일 경로

### 2. Emergency Support와 동일한 함수 사용
```python
from service.lang_chain.internal_external_lang_chain import (
    load_embedding_model,
    load_faiss_index,
    load_chunks,
    build_rag_chain,
    get_rag_answer_async
)
```

**코드 동일성**: `service/lang_chain/internal_external_lang_chain.py`는 `emergency_support_lang_chain.py`와 완전히 동일한 함수들을 제공합니다.

### 3. 내과/외과 질의 처리
```python
async def on_internal_external_ask_req(self, client_session, request: InternalExternalAskRequest) -> InternalExternalAskResponse:
    question = request.question
    answer = await get_rag_answer_async(
        question=question,
        index=self.index,
        chunks=self.chunks,
        embed_model=self.embed_model,
        rag_chain=self.rag_chain
    )
    response = InternalExternalAskResponse(answer=answer)
    return response
```

## 📊 요청/응답 스키마

### InternalExternalAskRequest
```python
class InternalExternalAskRequest(BaseRequest):
    question: str  # 내과/외과 관련 질문
```

### InternalExternalAskResponse  
```python
class InternalExternalAskResponse(BaseResponse):
    answer: str    # RAG 시스템이 생성한 응답
```

## 🔄 처리 플로우

```
내과/외과 질문
    ↓
InternalExternalTemplateImpl.on_internal_external_ask_req()
    ↓
get_rag_answer_async() 호출 (Emergency Support와 동일한 함수)
    ↓
RAG 응답 반환
```

## 🎯 내과/외과 전문성

이 템플릿이 다루는 내과/외과 구분:

- **내과 질환**: 내부 장기 질병, 만성질환, 약물치료 등
- **외과 질환**: 수술적 치료, 외상, 종양 등  
- **구분 기준**: 증상에 따른 적절한 진료과 추천
- **치료 방향**: 보존적 치료 vs 수술적 치료

## 🔗 의존성

### 사용하는 모듈
- `service.lang_chain.internal_external_lang_chain` - 함수 기반 RAG 시스템 (Emergency Support와 동일)
- `template.internal_external.common.internal_external_serialize` - 요청/응답 모델

### 사용하는 라이브러리
- `dotenv` - 환경변수 로드
- `os` - 환경변수 접근
- `asyncio` - 비동기 처리

## 🖥️ 로깅

**실제 구현된 로그 메시지**:
```python
print(f"Using INDEX_PATH: {INDEX_PATH}")
print(f"Using CHUNK_PATH: {CHUNK_PATH}")
print("Internal External Template initialized")
print("Emergency Support data loaded")      # 주목: Emergency Support 메시지 재사용
print("Emergency Support client created")   # 주목: Emergency Support 메시지 재사용
print("Emergency Support client updated")   # 주목: Emergency Support 메시지 재사용
print("Emergency Support client deleted")   # 주목: Emergency Support 메시지 재사용
```

**특이점**: 로그 메시지에서 "Emergency Support"라는 텍스트를 그대로 사용하여 코드 복사 흔적이 보입니다.

## 💭 실제 코드의 특징

1. **코드 재사용**: Emergency Support와 동일한 RAG 함수 사용
2. **초기화 방식 차이**: `__init__`에서 직접 초기화 (Emergency Support는 `init()` 메서드)
3. **상속 구조 차이**: BaseTemplate 미상속으로 독립적 구현
4. **환경변수 디버깅**: INDEX_PATH, CHUNK_PATH 출력으로 경로 확인
5. **로그 메시지 중복**: Emergency Support 메시지를 그대로 사용

## ⚖️ Emergency Support vs Internal External

| 구분 | Emergency Support | Internal External |
|------|------------------|-------------------|
| **상속** | EmergencySupportTemplate 상속 | BaseTemplate 미상속 |
| **초기화** | `init(config)` 메서드 | `__init__()` 생성자 |
| **RAG 함수** | 동일한 함수 사용 | 동일한 함수 사용 |
| **로그** | 고유 메시지 | Emergency Support 메시지 재사용 |

## 🧬 코드 동일성

`service/lang_chain/internal_external_lang_chain.py`와 `emergency_support_lang_chain.py`는 완전히 동일한 코드입니다. 이는:

1. **중복 코드 존재**: 동일한 RAG 로직의 복제
2. **벡터 DB 차이**: 각각 다른 의료 도메인 데이터 사용
3. **환경변수 분리**: 각각 독립된 벡터 DB 경로 사용

이 모듈은 **내과/외과 전문 상담사**로서 증상과 질병을 기반으로 적절한 진료과 추천과 치료 방향을 제시하는 **전문 RAG 시스템**입니다.