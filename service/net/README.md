# Net Service Module

## 📌 모듈 개요
Net 서비스는 네트워크 통신의 기본 프로토콜 구조를 정의하는 모듈입니다. API 요청/응답의 공통 스키마를 제공합니다.

## 🎯 왜 독립 모듈인가?

### 단일 파일 구성
```
net/
└── protocol_base.py  # 기본 요청/응답 모델
```

**독립 모듈인 이유**:
- **프로토콜 표준화**: 모든 API 통신의 기본 형식 정의
- **타입 안정성**: Pydantic 모델로 데이터 검증
- **재사용성**: 모든 엔드포인트에서 상속하여 사용

## 🏗️ 실제 구현 분석

### BaseRequest 클래스
```python
class BaseRequest(BaseModel):
    accessToken: str = ""  # 인증 토큰
    sequence: int = 0      # 요청 시퀀스 번호
```

**설계 의도**:
- `accessToken`: 모든 요청에 인증 정보 포함
- `sequence`: 요청 추적 및 중복 방지

### BaseResponse 클래스
```python
class BaseResponse(BaseModel):
    errorCode: int = 0     # 에러 코드 (0 = 성공)
    sequence: int = 0      # 응답 시퀀스 번호
```

**설계 의도**:
- `errorCode`: 표준화된 에러 처리
- `sequence`: 요청-응답 매칭

## 💡 핵심 설계 원칙

### 1. 상속 기반 확장
```python
# 다른 모듈에서 사용 예시
class LoginRequest(BaseRequest):
    username: str
    password: str

class LoginResponse(BaseResponse):
    userId: str
    sessionId: str
```

### 2. Pydantic 활용
- **자동 검증**: 타입 체크와 데이터 검증
- **직렬화**: JSON ↔ Python 객체 자동 변환
- **문서화**: OpenAPI 스키마 자동 생성

### 3. 기본값 제공
- `""` (빈 문자열): 선택적 토큰
- `0`: 초기 시퀀스 및 성공 코드

## 🔄 프로토콜 플로우

```
클라이언트                     서버
    |                           |
    |-- BaseRequest 상속 ------>|
    |   (accessToken, sequence) |
    |                           |
    |                         검증
    |                         처리
    |                           |
    |<-- BaseResponse 상속 -----|
    |   (errorCode, sequence)   |
```

## 📊 실제 사용 패턴

### 1. 인증 체크
```python
# cache/dependencies.py에서 사용
async def require_session(request: Request):
    body = await request.json()
    access_token = body.get("accessToken")  # BaseRequest의 accessToken
```

### 2. 에러 코드 표준화
```python
# 성공: errorCode = 0
# 실패: errorCode > 0 (각 에러마다 고유 코드)
```

## 🎓 코드에서 확인된 설계 의도

1. **최소한의 공통 필드**: 필수 요소만 포함
2. **확장 가능한 구조**: 상속을 통한 커스터마이징
3. **타입 안정성**: Pydantic BaseModel 활용
4. **프로토콜 일관성**: 모든 API가 동일한 기본 구조

## 🔗 다른 모듈과의 관계

### 사용되는 곳
- **template 모듈**: 각 템플릿의 요청/응답 모델 기반
- **application 라우터**: API 엔드포인트 스키마 정의
- **cache/dependencies.py**: 세션 검증 시 참조

## ⚠️ 실제 코드의 특징

1. **간결성**: 9줄의 짧은 코드로 핵심 기능 구현
2. **기본값 설정**: 모든 필드에 기본값 제공
3. **타입 힌팅**: 명확한 타입 정의
4. **Pydantic 의존**: FastAPI와 완벽 호환

## 💭 이 모듈의 역할

이 모듈은 **"프로토콜 계층"**의 기초를 제공합니다:
- 네트워크 통신의 최소 단위 정의
- 확장 가능한 기본 구조 제공
- 타입 안정성과 검증 보장

작지만 중요한 모듈로, 전체 API 통신의 기반이 됩니다.