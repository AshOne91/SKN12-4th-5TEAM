# Category Template Module

## 📌 모듈 개요
Category 템플릿은 **의료 질문 분류 및 라우팅 시스템**을 구현합니다. 사용자 질문을 적절한 의료 도메인으로 분류하고, 해당 도메인의 전용 서버로 라우팅하는 역할을 담당합니다.

## 🏗️ 실제 구조

```
template/category/
├── category_template_impl.py  # 분류 비즈니스 로직 구현
└── common/
    └── category_serialize.py  # 요청/응답 스키마
```

## 🤖 핵심 기능 분석

### 1. CategoryTemplateImpl 클래스
```python
class CategoryTemplateImpl(CategoryTemplate):
    def __init__(self):
        super().__init__()
        self.category_classifier = Category_Classifier()  # 분류기 인스턴스
        self.http_client_pool = HTTPClientPool()         # HTTP 클라이언트 풀
```

**실제 구현 특징**:
- `Category_Classifier` 인스턴스를 `__init__`에서 생성
- `HTTPClientPool` 인스턴스를 미리 생성하여 재사용
- 프레임워크 호환성을 위한 별도 `init(config)` 메서드 제공

### 2. 질문 분류 및 라우팅
```python
async def on_category_ask_req(self, client_session, request: CategoryAskRequest) -> CategoryAskResponse:
    question = request.question
    
    # 1. Category_Classifier로 카테고리 분류
    category = self.category_classifier.return_category(user_input=question)
    
    # 2. 카테고리에 따른 URL 매핑
    url = CATEGORY_URLS.get(category)
    
    # 3. 해당 서비스로 HTTP 요청
    if url:
        resp = await self.http_client_pool.post(url=url, json={"question": question})
        data = resp.json()
        response = CategoryAskResponse(answer=data.get("answer", ""))
    else:
        response = CategoryAskResponse(answer="")
```

## 🌐 서비스 라우팅 매핑

### CATEGORY_URLS 환경변수 매핑
```python
CATEGORY_URLS = {
    "emergency_support": os.getenv("EMERGENCY_SUPPORT_URL"),
    "internal_external": os.getenv("INTERNAL_EXTERNAL_URL"),
    "drug": os.getenv("DRUG_URL"),
    "clinic": os.getenv("CLINIC_URL"),
}
```

**실제 사용되는 환경변수**:
- `EMERGENCY_SUPPORT_URL`
- `INTERNAL_EXTERNAL_URL` 
- `DRUG_URL`
- `CLINIC_URL`

## 📊 요청/응답 스키마

### CategoryAskRequest
```python
class CategoryAskRequest(BaseRequest):
    question: str  # 분류할 질문
```

### CategoryAskResponse  
```python
class CategoryAskResponse(BaseResponse):
    answer: str    # 분류된 서비스의 응답
```

## 🔄 처리 플로우

```
사용자 질문
    ↓
Category_Classifier.return_category()
    ↓
카테고리 → URL 매핑 (CATEGORY_URLS)
    ↓
HTTPClientPool.post() → 해당 서비스
    ↓
외부 서비스 응답 → CategoryAskResponse
```

## ⚡ 에러 처리

### HTTP 요청 에러 처리
```python
try:
    resp = await self.http_client_pool.post(url=url, json={"question": question})
    resp.raise_for_status()  # 4xx/5xx 상태 코드 예외 발생
    data = resp.json()
except Exception as e:
    print(f"Error calling external service {url}: {e}")
    data = {"answer": f"죄송합니다. 서비스 연결에 문제가 발생했습니다. ({e})"}
```

**실제 구현된 에러 처리**:
- `raise_for_status()`로 HTTP 에러 감지
- 서비스 연결 실패 시 사용자 친화적 메시지 반환
- URL이 없는 경우 빈 답변 반환

## 🔗 의존성

### 사용하는 모듈
- `service.lang_chain.category_classifer.Category_Classifier`
- `service.http.http_client.HTTPClientPool`
- `template.category.common.category_serialize`

### 사용하는 라이브러리
- `dotenv` - 환경변수 로드
- `os` - 환경변수 접근

## 🖥️ 로깅

**실제 구현된 로그 메시지**:
```python
print(f"Classified category: '{category}'")
print(f"Looked up URL: '{url}' for category '{category}'") 
print(f"Error calling external service {url}: {e}")
print(f"No matching URL found for category '{category}'. Returning empty answer.")
```

## 💭 실제 코드의 특징

1. **리소스 효율성**: 분류기와 HTTP 클라이언트를 한 번만 생성하여 재사용
2. **에러 안정성**: HTTP 요청 실패 시 사용자에게 친화적 메시지 제공
3. **확장성**: 새로운 카테고리 추가 시 `CATEGORY_URLS`에 추가만 하면 됨
4. **디버깅 지원**: 상세한 로그를 통한 분류 과정 추적

이 모듈은 **의료 질문 라우터**로서 전체 시스템의 **트래픽 제어 허브** 역할을 담당합니다.