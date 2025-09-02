# LangChain Service Module

## 📌 모듈 개요
LangChain 서비스는 의료 도메인별 AI 응답 시스템을 구현합니다. RAG(Retrieval-Augmented Generation) 패턴을 통해 벡터 검색과 LLM을 결합한 지능형 응답을 제공합니다.

## 🎯 왜 이 파일들이 함께 묶여있는가?

### 파일 구성과 역할
```
lang_chain/
├── category_classifer.py           # 카테고리 분류 + 챗봇 (클래스 기반)
├── drug_lang_chain.py              # 약품 정보 RAG (클래스 기반)
├── emergency_support_lang_chain.py # 응급 지원 RAG (함수 기반)
└── internal_external_lang_chain.py # 내과/외과 RAG (함수 기반, emergency와 동일)
```

**공통 기술 스택**:
- `SentenceTransformer("jhgan/ko-sroberta-multitask")`: 한국어 임베딩 모델
- `FAISS`: 벡터 유사도 검색
- `ChatOpenAI(model="gpt-4o-mini")`: OpenAI LLM
- `LangChain`: 프롬프트 템플릿과 체인 구성

## 🏗️ 실제 구현 분석

### 1. Category Classifier (카테고리 분류기)

```python
class Category_Classifier:
    def __init__(self):
        # 벡터 DB 로드 (pickle, torch 파일)
        self.category_texts, self.category_categories, self.category_embeddings = self.load_vector_db()
        # 정규화된 임베딩
        self.category_embeddings_norm = self.normalize(self.category_embeddings.numpy())
        # 한국어 임베딩 모델
        self.embedder = SentenceTransformer("jhgan/ko-sroberta-multitask")
        # 두 가지 LLM 사용
        self.chatbot_llm = ChatOpenAI(...)  # LangChain용
        self.client = OpenAI(...)           # 분류 전용
```

**특징**:
- 두 가지 LLM 클라이언트 사용 (LangChain + OpenAI SDK)
- pickle과 torch 파일로 벡터 DB 관리
- 벡터 정규화로 코사인 유사도 계산 최적화

### 2. Drug Vector Store (약품 정보)

```python
class Vector_store:
    def __init__(self, api_key, chunk_path, index_path, ...):
        self.chunks = self.load_chunks(chunk_path)      # 텍스트 청크
        self.index = self.load_faiss_index(index_path)  # FAISS 인덱스
        self.embedding_model = self.load_embedding_model(...)
        self.llm = self.connect_gpt(...)
        self.rag_chain = self.build_rag_chain()
```

**특징**:
- 텍스트 파일에서 청크 로드
- FAISS 인덱스 파일 사용
- RAG 체인 빌드 패턴

### 3. Emergency & Internal/External (응급/내외과)

```python
# 함수 기반 구현
def load_embedding_model():
    return SentenceTransformer("jhgan/ko-sroberta-multitask")

def load_faiss_index(index_path: str):
    return faiss.read_index(index_path)

async def get_rag_answer_async(question, index, chunks, embed_model, rag_chain):
    # 1. 검색
    top_chunks = search_similar_chunks(question, index, chunks, embed_model)
    # 2. 생성
    answer = await rag_chain.ainvoke({"context": context, "question": question})
```

**특징**:
- 함수 기반 모듈화
- 비동기 처리 (`async/await`)
- emergency와 internal_external은 **완전히 동일한 코드**

## 💡 핵심 구현 패턴

### 1. RAG 처리 흐름
```python
# 1. 질문을 벡터로 변환
embedding = model.encode([question])

# 2. FAISS로 유사 문서 검색
_, indices = index.search(embedding, top_k)

# 3. 검색된 문서를 컨텍스트로 구성
context = "\n".join(top_chunks)

# 4. LLM에 컨텍스트와 질문 전달
answer = await rag_chain.ainvoke({"context": context, "question": question})
```

### 2. 프롬프트 템플릿
```python
# 의료 전문 프롬프트
"당신은 의학전공을 하여 저희의 질문에 대답을 잘 해주는 챗봇입니다"
"만약 진료혹은 약, 의학과 관련이 없는 질문이면 질문이 주제와 다르다고 하면 됩니다"
```

### 3. 벡터 정규화
```python
def normalize(self, v):
    return v / (np.linalg.norm(v, axis=-1, keepdims=True) + 1e-8)
```
- L2 정규화로 단위 벡터 생성
- 코사인 유사도 계산 최적화

## 🔄 데이터 플로우

```
사용자 질문
    ↓
임베딩 생성 (SentenceTransformer)
    ↓
FAISS 검색 (top_k=3)
    ↓
청크 추출
    ↓
프롬프트 구성
    ↓
ChatGPT 호출 (gpt-4o-mini)
    ↓
응답 반환
```

## ⚡ 실제 사용된 최적화

### 1. 벡터 검색 최적화
- `float32` 타입 변환으로 FAISS 호환성 확보
- top_k=3으로 관련성 높은 문서만 선택

### 2. 비동기 처리
- `ainvoke` 사용으로 non-blocking 처리
- FastAPI와의 비동기 통합

### 3. 리소스 재사용
- 모델과 인덱스를 한 번만 로드
- 클래스/모듈 레벨에서 재사용

## 📊 실제 파일 구조와 데이터

### 벡터 DB 파일 형식
- **Category**: `texts.pkl`, `categories.pkl`, `embeddings.pt`
- **Drug/Emergency**: `*.txt` (청크), `*.index` (FAISS)

### 환경 변수 사용
```python
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CATEGORY_VECTORDB = os.getenv('CATEGORY_VECTORDB')
```

## 🎓 코드에서 확인된 설계 의도

1. **도메인 분리**: 각 의료 분야별 독립된 파일
2. **구현 방식 다양성**: 클래스 기반 vs 함수 기반
3. **코드 재사용**: emergency와 internal_external 동일 코드
4. **한국어 특화**: ko-sroberta-multitask 모델 사용
5. **경량 모델**: gpt-4o-mini로 비용 최적화

## 🔗 실제 의존성

### 외부 라이브러리
- `sentence_transformers`: 임베딩 생성
- `faiss`: 벡터 검색
- `langchain_core`, `langchain_openai`: LLM 체인
- `openai`: OpenAI API 직접 호출
- `numpy`, `torch`, `pickle`: 데이터 처리

### 리소스 의존
- `resources/vectorDB/`: 실제 벡터 데이터 저장 위치
- `.env`: API 키 및 경로 설정

## ⚠️ 코드에서 발견된 주의사항

1. **중복 코드**: emergency와 internal_external 완전 동일
2. **혼재된 방식**: 클래스와 함수 기반 혼용
3. **에러 처리 부재**: 파일 로드 실패 시 처리 없음
4. **하드코딩된 값**: top_k=3, temperature=0 등