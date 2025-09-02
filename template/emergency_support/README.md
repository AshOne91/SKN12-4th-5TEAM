# Emergency Support Template Module

## 📌 모듈 개요
Emergency Support 템플릿은 **응급 의료 지원 RAG 시스템**을 구현합니다. 함수 기반의 RAG 모듈을 사용하여 응급 상황 관련 질문에 대한 전문적인 응답을 제공합니다.

## 🏗️ 실제 구조

```
template/emergency_support/
├── emergency_support_template_impl.py  # 응급 지원 RAG 로직 구현
└── common/
    └── emergency_support_serialize.py  # 요청/응답 스키마
```

## 🤖 핵심 기능 분석

### 1. EmergencySupportTemplateImpl 초기화
```python
class EmergencySupportTemplateImpl(EmergencySupportTemplate):
    def init(self, config):
        # RAG 리소스 로드
        self.embed_model = load_embedding_model()
        self.index = load_faiss_index(INDEX_PATH)
        self.chunks = load_chunks(CHUNK_PATH)
        self.rag_chain = build_rag_chain(OPENAI_API_KEY)
```

**실제 사용되는 환경변수**:
- `OPENAI_API_KEY` - OpenAI API 키
- `EMERGENCY_SUPPORT_VECTORDB_INDEX` - FAISS 인덱스 파일 경로
- `EMERGENCY_SUPPORT_VECTORDB_TXT` - 응급 지원 텍스트 파일 경로

### 2. 함수 기반 RAG 모듈 사용
```python
from service.lang_chain.emergency_support_lang_chain import (
    load_embedding_model,
    load_faiss_index,
    load_chunks,
    build_rag_chain,
    get_rag_answer_async
)
```

**특징**:
- 클래스가 아닌 **함수 기반** 모듈 사용
- 각 컴포넌트를 별도 함수로 로드
- 모듈러 구조로 재사용성 높임

### 3. 응급 지원 질의 처리
```python
async def on_emergency_support_ask_req(self, client_session, request: EmergencySupportAskRequest) -> EmergencySupportAskResponse:
    question = request.question
    answer = await get_rag_answer_async(
        question=question,
        index=self.index,
        chunks=self.chunks,
        embed_model=self.embed_model,
        rag_chain=self.rag_chain
    )
    response = EmergencySupportAskResponse(answer=answer)
    return response
```

## 📊 요청/응답 스키마

### EmergencySupportAskRequest
```python
class EmergencySupportAskRequest(BaseRequest):
    question: str  # 응급 상황 관련 질문
```

### EmergencySupportAskResponse
```python
class EmergencySupportAskResponse(BaseResponse):
    answer: str    # RAG 시스템이 생성한 응답
```

## 🔄 처리 플로우

```
응급 상황 질문
    ↓
EmergencySupportTemplateImpl.on_emergency_support_ask_req()
    ↓
get_rag_answer_async() 호출
    ↓ 
RAG 응답 반환
```

## ⚡ RAG 컴포넌트 구성

### 1. 임베딩 모델
```python
self.embed_model = load_embedding_model()
```

### 2. FAISS 인덱스
```python
self.index = load_faiss_index(INDEX_PATH)
```

### 3. 문서 청크
```python
self.chunks = load_chunks(CHUNK_PATH)
```

### 4. RAG 체인
```python
self.rag_chain = build_rag_chain(OPENAI_API_KEY)
```

## 🔗 의존성

### 사용하는 모듈
- `service.lang_chain.emergency_support_lang_chain` - 함수 기반 RAG 시스템
- `template.emergency_support.common.emergency_support_serialize` - 요청/응답 모델
- `template.base.template.emergency_support_template.EmergencySupportTemplate` - 기본 템플릿

### 사용하는 라이브러리
- `dotenv` - 환경변수 로드
- `os` - 환경변수 접근
- `asyncio` - 비동기 처리

## 🖥️ 로깅

**실제 구현된 로그 메시지**:
```python
print("Emergency Support data loaded")
print("Emergency Support client created")
print("Emergency Support client updated")
print("Emergency Support client deleted")
```

## 💭 실제 코드의 특징

1. **함수 기반 아키텍처**: 클래스가 아닌 함수로 RAG 컴포넌트 구성
2. **지연 초기화**: `init()` 메서드에서 RAG 리소스 로드
3. **모듈러 설계**: 각 RAG 컴포넌트를 독립적인 함수로 분리
4. **비동기 지원**: `get_rag_answer_async()`로 non-blocking 처리
5. **파라미터 전달**: 모든 필요한 컴포넌트를 명시적으로 전달

## 🚨 응급 의료 전문성

Emergency Support 템플릿은 다음과 같은 응급 상황에 특화된 정보를 제공합니다:

- 응급처치 방법
- 증상별 대응 요령
- 응급실 방문 기준
- 응급 약물 정보
- 응급상황 판단 가이드

## 🔧 함수 기반 vs 클래스 기반

Drug 템플릿의 클래스 기반 `Vector_store`와 달리, Emergency Support는 **함수 기반** 구조를 사용합니다:

```python
# Drug (클래스 기반)
self.vector_store = Vector_store(...)
answer = await self.vector_store.rag_answer(question)

# Emergency Support (함수 기반)  
answer = await get_rag_answer_async(question, index, chunks, embed_model, rag_chain)
```

이는 **구현 방식의 다양성**을 보여주며, 각각의 장단점이 있습니다:
- **함수 기반**: 더 명시적이고 테스트하기 쉬움
- **클래스 기반**: 상태 관리와 캡슐화에 유리

이 모듈은 **응급 의료 전문가**로서 생명과 직결된 응급 상황에서 정확하고 신속한 의료 정보를 제공하는 **전문 RAG 시스템**입니다.