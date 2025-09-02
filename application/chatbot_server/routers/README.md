# Chatbot Server Routers

## 📌 개요
Chatbot Server의 API 라우터 모듈입니다. 인증(Account), 챗봇(Chatbot), 테스트(Test) 관련 HTTP 엔드포인트를 제공합니다.

## 🏗️ 구조
```
application/chatbot_server/routers/
├── __init__.py
├── account.py       # 인증 API 라우터
├── chatbot.py       # 챗봇 API 라우터
└── test.py          # 테스트 API 라우터
```

## 🔐 account.py

### POST /login
```python
@router.post("/login", response_model=AccountLoginResponse)
async def account_login(request: AccountLoginRequest, req: Request):
```

**기능**: 사용자 로그인 처리

**파라미터**:
- `mysql = req.app.state.globaldb` - 글로벌 DB 연결
- `req.app` - FastAPI 애플리케이션 인스턴스 전달

### POST /logout
```python
@router.post("/logout", response_model=AccountLogoutResponse)
async def account_logout(request: AccountLogoutRequest, req: Request):
```

**기능**: 사용자 로그아웃 처리

### POST /signup
```python
@router.post("/signup", response_model=AccountSignupResponse)
async def account_signup(request: AccountSignupRequest, req: Request):
```

**기능**: 사용자 회원가입 처리

**파라미터**:
- `mysql = req.app.state.globaldb` - 글로벌 DB 연결

## 💬 chatbot.py

챗봇 관련 API 엔드포인트들:
- 채팅방 관리 (생성, 목록 조회)
- 메시지 전송 및 응답
- 대화 히스토리 관리

## 🧪 test.py

테스트 및 개발용 API 엔드포인트들을 제공합니다.

## 💡 공통 코드 패턴

### 템플릿 조회 및 검증
```python
account_template = TemplateContext.get_template(TemplateType.ACCOUNT)
if account_template is None:
    raise RuntimeError("AccountTemplateImpl is not registered in TemplateContext")
```

### 상태 접근
```python
mysql = req.app.state.globaldb  # 글로벌 DB 풀
```

### 템플릿 위임
```python
return await account_template.on_account_login_req(None, request, mysql, req.app)
```

**특징**:
- `client_session`에 `None` 전달
- DB 연결과 앱 인스턴스를 직접 전달
- 모든 비즈니스 로직을 템플릿에 위임

이 라우터들은 **HTTP 프로토콜과 템플릿 계층 간의 어댑터** 역할을 담당합니다.