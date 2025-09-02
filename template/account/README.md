# Account Template Module

## 📌 모듈 개요
Account 템플릿은 **사용자 인증과 계정 관리**를 담당하는 비즈니스 로직 모듈입니다. 회원가입, 로그인, 로그아웃 기능을 제공하며, 샤딩을 지원하는 확장 가능한 아키텍처를 구현합니다.

## 🏗️ 실제 구조

```
template/account/
├── account_template_impl.py  # 계정 비즈니스 로직 구현
└── common/
    ├── account_model.py     # 데이터 모델 (빈 파일)
    └── account_serialize.py # 요청/응답 스키마
```

## 🔐 핵심 기능 분석

### 1. 회원가입 시스템
```python
async def on_account_signup_req(self, ...):
    # 1. 중복 아이디 체크
    rows = await mysql_global.execute(
        "SELECT 1 FROM users WHERE username=%s", (request.id,)
    )
    
    # 2. salt 생성 및 비밀번호 해시 (SHA256)
    salt = os.urandom(16).hex()
    password_hash = hashlib.sha256((request.password + salt).encode()).hexdigest()
    
    # 3. 샤드 할당 (RegisterUser 프로시저)
    result = await mysql_global.call_procedure("RegisterUser", 
        (request.id, "", password_hash, salt, shard_count))
    
    # 4. 자동 로그인 처리
    access_token = str(uuid.uuid4())
    session_info = SessionInfo(user_id=user_id, shard_id=shard_id)
    await set_session_info(access_token, session_info)
```

**특징**:
- **보안**: SHA256 + 랜덤 salt로 비밀번호 해싱
- **샤딩**: 회원가입 시 자동 샤드 할당
- **UX**: 회원가입 후 자동 로그인

### 2. 로그인 시스템
```python
async def on_account_login_req(self, ...):
    # 1. 사용자 조회
    rows = await mysql_global.execute(
        "SELECT user_id, password_hash, salt FROM users WHERE username=%s"
    )
    
    # 2. 비밀번호 검증
    hash_input = (request.password + salt).encode("utf-8")
    hashed = hashlib.sha256(hash_input).hexdigest()
    if hashed != password_hash:
        return AccountLoginResponse(errorCode=401)
    
    # 3. 샤드 매핑 조회
    rows = await mysql_global.execute(
        "SELECT shard_id FROM user_shard_mapping WHERE user_id=%s"
    )
    
    # 4. 세션 생성
    access_token = str(uuid.uuid4())
    await set_session_info(access_token, session_info)
```

**특징**:
- **다단계 검증**: 사용자 존재 → 비밀번호 → 샤드 매핑
- **UUID 토큰**: 예측 불가능한 세션 토큰
- **샤드 인식**: 사용자별 샤드 정보 포함

### 3. 로그아웃 시스템
```python
async def on_account_logout_req(self, ...):
    access_token = request.accessToken
    await remove_session_info(access_token)  # Redis에서 세션 제거
    return AccountLogoutResponse()
```

**특징**:
- **세션 무효화**: Redis에서 즉시 제거
- **간단한 구현**: 토큰만으로 처리

## 📊 요청/응답 스키마

### 회원가입
```python
class AccountSignupRequest(BaseRequest):
    id: str                      # 아이디 (필수)
    password: str               # 비밀번호 (필수)
    name: Optional[str] = None  # 이름 (선택)
    phone: Optional[str] = None # 전화번호 (선택)

class AccountSignupResponse(BaseResponse):
    message: Optional[str] = None  # 성공시 access_token 반환
```

### 로그인
```python
class AccountLoginRequest(BaseRequest):
    id: str       # 아이디
    password: str # 비밀번호

class AccountLoginResponse(BaseResponse):
    accessToken: str  # 세션 토큰
```

### 로그아웃
```python
class AccountLogoutRequest(BaseRequest):
    pass  # accessToken은 BaseRequest에서 상속

class AccountLogoutResponse(BaseResponse):
    pass  # 기본 응답만 사용
```

## 🗄️ 데이터베이스 설계

### 사용된 테이블
1. **users**: 사용자 기본 정보
   - `user_id`, `username`, `password_hash`, `salt`

2. **user_shard_mapping**: 샤드 매핑
   - `user_id`, `shard_id`

### 프로시저
- **RegisterUser**: 회원가입 + 샤드 할당을 원자적으로 처리

## 🏃‍♂️ 실제 처리 플로우

### 회원가입 플로우
```
1. 중복 아이디 체크
    ↓
2. salt 생성 + 비밀번호 해싱
    ↓  
3. RegisterUser 프로시저 호출
   (users 테이블 + user_shard_mapping 테이블)
    ↓
4. 자동 로그인 (세션 생성)
    ↓
5. access_token 반환
```

### 로그인 플로우
```
1. username으로 사용자 조회
    ↓
2. salt + 비밀번호 해싱하여 검증
    ↓
3. user_shard_mapping에서 샤드 조회
    ↓
4. SessionInfo 생성 (shard_id 포함)
    ↓
5. Redis에 세션 저장
    ↓
6. access_token 반환
```

## 🔒 보안 구현

### 1. 비밀번호 보안
- **Salting**: 각 사용자마다 고유한 16바이트 랜덤 salt
- **SHA256**: 단방향 해시 함수 사용
- **No Plain Text**: 비밀번호 원문 절대 저장 안함

### 2. 세션 보안
- **UUID4**: 예측 불가능한 세션 토큰
- **TTL**: Redis 세션 자동 만료
- **상태 관리**: ClientSessionState로 세션 상태 추적

## 📈 샤딩 지원

### 샤드 할당 로직
```python
shard_count = len(app.state.userdb_pools)  # 현재 활성 샤드 수
result = await mysql_global.call_procedure("RegisterUser", 
    (request.id, "", password_hash, salt, shard_count))
```

**특징**:
- 동적 샤드 수 계산
- 프로시저 내부에서 샤드 할당 알고리즘 구현
- 글로벌 DB에서 매핑 정보 관리

## ⚠️ 코드에서 발견된 이슈

### 1. 중복 import
```python
from service.cache.async_session import set_session_info  # 7번째 줄에 중복
```

### 2. 에러 코드 하드코딩
- 404, 401, 409, 500 등 매직 넘버 사용
- 에러 코드 상수 정의 필요

### 3. 일관성 부족
- 회원가입 응답의 `message`에 `access_token` 반환 (네이밍 불일치)

## 🎓 이 모듈에서 배울 수 있는 것

1. **안전한 인증**: Salt + Hash 비밀번호 저장
2. **샤딩 아키텍처**: 수평 확장을 위한 데이터 분할
3. **세션 관리**: Redis를 활용한 무상태 세션
4. **프로시저 활용**: 복잡한 비즈니스 로직의 원자적 처리
5. **에러 처리**: 다양한 실패 시나리오 대응

## 🔗 다른 모듈과의 연결

- **service/cache**: 세션 저장/조회
- **service/db**: 사용자 데이터 CRUD
- **service/net**: 요청/응답 프로토콜
- **application/chatbot_server**: API 엔드포인트 제공

이 모듈은 **인증 시스템의 핵심**으로, 모든 보안의 출발점이 됩니다.