# Category Server Routers

## 📌 개요
Category Server의 API 라우터 모듈입니다. 의료 질문 분류 관련 HTTP 엔드포인트를 제공합니다.

## 🏗️ 구조
```
application/category_server/routers/
├── __init__.py
└── category.py      # 분류 API 라우터
```

## 🔗 API 엔드포인트

### category.py

#### POST /ask
```python
@router.post("/ask", response_model=CategoryAskResponse)
async def category_ask(request: CategoryAskRequest):
```

**기능**: 의료 질문을 분류하고 해당 도메인 서버로 라우팅하여 응답 반환

**요청**: `CategoryAskRequest`
- `question: str` - 분류할 의료 질문

**응답**: `CategoryAskResponse`  
- `answer: str` - 분류된 도메인 서버의 응답

**처리 플로우**:
1. `TemplateContext.get_template(TemplateType.CATEGORY)` - 카테고리 템플릿 조회
2. 템플릿 등록 검증 (`RuntimeError` 발생 가능)
3. `category_template.on_category_ask_req(None, request)` - 템플릿에 처리 위임

## 💡 실제 코드 특징

1. **템플릿 위임 패턴**: 비즈니스 로직을 템플릿에 완전히 위임
2. **에러 처리**: 템플릿 미등록 시 `RuntimeError` 발생
3. **세션 무시**: `client_session` 파라미터에 `None` 전달
4. **타입 안전성**: `response_model` 명시로 응답 스키마 검증

이 라우터는 **HTTP ↔ 템플릿 브리지** 역할을 담당하는 얇은 어댑터 레이어입니다.