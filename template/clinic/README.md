# Clinic Template Module

## 📌 모듈 개요
Clinic 템플릿은 **병원 및 의료 정보 RAG 시스템**을 구현합니다. FAISS 벡터 검색과 GPT-4o를 결합하여 의료진/병원 관련 질문에 대한 정확한 응답을 제공합니다.

## 🏗️ 실제 구조

```
template/clinic/
├── clinic_template_impl.py  # 병원 정보 RAG 로직 구현
└── common/
    └── clinic_serialize.py  # 요청/응답 스키마
```

## 🤖 핵심 기능 분석

### 1. ClinicTemplateImpl 초기화
```python
class ClinicTemplateImpl(ClinicTemplate):
    def init(self, config):
        # FAISS 인덱스 로드
        self.index = faiss.read_index(os.path.join(base_path, "faiss_index", "index.faiss"))
        
        # 문서 ID 매핑 로드
        with open(os.path.join(base_path, "doc_ids.json"), "r", encoding="utf-8") as f:
            self.doc_ids = json.load(f)
            
        # 임베딩 모델 초기화
        self.embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        
        # OpenAI 클라이언트 초기화
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # 키워드 인덱스 로드
        with open("resources/vectorDB/treatment/RAG_Output/faiss_medical/keyword_index.json") as f:
            self.keyword_index = json.load(f)
```

**실제 사용되는 환경변수**:
- `CLINIC_VECTORDB_BASE` - FAISS 인덱스와 문서 ID 파일 경로
- `CLINIC_VECTORDB_DOCS` - 처리된 문서 파일들 경로  
- `OPENAI_API_KEY` - OpenAI API 키

### 2. RAG 처리 플로우
```python
async def on_clinic_ask_req(self, client_session, request: ClinicAskRequest) -> ClinicAskResponse:
    question = request.question
    
    # 1. 질문 임베딩
    q_vector = self.embedding_model.encode(question)
    q_vector = np.array([q_vector]).astype("float32")
    
    # 2. FAISS 검색 (top 3)
    D, I = self.index.search(q_vector, k=3)
    
    # 3. 문서 chunk 로드
    retrieved_texts = []
    for idx in I[0]:
        if idx < len(self.doc_ids):
            doc_filename = self.doc_ids[idx]
            if not doc_filename.endswith(".txt"):
                doc_filename += ".txt"
            # 파일 내용 읽기
    
    context = "\n\n".join(retrieved_texts)
```

## 🔍 키워드 Fallback 시스템

### 키워드 추출 및 정제
```python
# 한국어 키워드 추출
raw_keywords = re.findall(r"[가-힣a-zA-Z]{2,}", question)

# 조사 제거
particles = {"은", "는", "이", "가", "을", "를", "에", "의", "으로", "에서", "도", "만", "와", "과", "보다"}
cleaned_keywords = []
for word in raw_keywords:
    for p in particles:
        if word.endswith(p) and len(word) > len(p):
            word = word[: -len(p)]
            break
    cleaned_keywords.append(word)
```

### Fallback 검색 로직
```python
# 키워드가 컨텍스트에 없으면 키워드 인덱스에서 추가 검색
if not any(k in context for k in question_keywords):
    fallback_limit = 4
    fallback_added = 0
    for kw in question_keywords:
        for fname in self.keyword_index.get(kw, []):
            # 추가 문서 로드하여 컨텍스트에 추가
```

## 📊 요청/응답 스키마

### ClinicAskRequest
```python
class ClinicAskRequest(BaseRequest):
    question: str  # 병원/의료진 관련 질문
```

### ClinicAskResponse
```python
class ClinicAskResponse(BaseResponse):
    answer: str    # GPT가 생성한 응답
```

## 🧠 GPT-4o 프롬프트 시스템

### 실제 사용되는 프롬프트
```python
prompt = f"""
당신은 신뢰할 수 있는 의료 전문 상담 AI입니다.

아래 [문서 내용]에 기반하여 [질문]에 정확하게 답변하세요.
문서에 정보가 없으면 "문서에서 해당 질문에 대한 정보를 찾을 수 없습니다."라고 말하세요.
절대 정보를 추측하거나 지어내지 마세요.

[문서 내용]
{context}

[질문]
{question}

[답변]
"""
```

### GPT 호출 파라미터
```python
response = self.client.chat.completions.create(
    model="gpt-4o",          # GPT-4o 모델 사용
    messages=[
        {"role": "system", "content": "너는 의료 전문 상담 AI야."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.2,         # 일관성 위한 낮은 temperature
    max_tokens=512,          # 응답 길이 제한
)
```

## ⚡ 성능 최적화

### 1. 컨텍스트 길이 제한
```python
MAX_CONTEXT_CHARS = 10_000
if len(context) > MAX_CONTEXT_CHARS:
    context = context[:MAX_CONTEXT_CHARS] + "\n\n...(생략됨)"
```

### 2. 파일 존재 검증
```python
if os.path.exists(doc_path):
    with open(doc_path, "r", encoding="utf-8") as f:
        content = f.read()
        if content.strip():
            retrieved_texts.append(content)
        else:
            print(f"파일은 있으나 내용이 비어 있음: {doc_filename}")
```

## 🔗 의존성

### 사용하는 라이브러리
- `sentence_transformers` - SentenceTransformer 임베딩
- `faiss` - 벡터 유사도 검색
- `openai` - GPT-4o API 호출
- `numpy` - 벡터 연산
- `json` - JSON 파일 처리
- `os` - 환경변수 및 파일 시스템
- `re` - 정규식 패턴 매칭
- `dotenv` - 환경변수 로드

### 데이터 파일 구조
- `{CLINIC_VECTORDB_BASE}/faiss_index/index.faiss` - FAISS 벡터 인덱스
- `{CLINIC_VECTORDB_BASE}/doc_ids.json` - 문서 ID 매핑
- `{CLINIC_VECTORDB_DOCS}/*.txt` - 처리된 문서 텍스트 파일들
- `resources/vectorDB/treatment/RAG_Output/faiss_medical/keyword_index.json` - 키워드 매핑

## 💭 실제 코드의 특징

1. **이중 검색 시스템**: FAISS 벡터 검색 + 키워드 fallback
2. **한국어 최적화**: 조사 제거를 통한 키워드 정제
3. **메모리 관리**: 컨텍스트 길이 제한으로 토큰 사용량 제어
4. **에러 안정성**: 파일 존재 확인 및 빈 파일 처리
5. **정확성 우선**: 문서 기반 답변, 추측 금지 프롬프트

이 모듈은 **의료 정보 전문가**로서 정확하고 신뢰할 수 있는 병원/의료진 정보를 제공하는 **RAG 시스템**입니다.