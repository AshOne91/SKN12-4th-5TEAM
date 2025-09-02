# Account Template Common Module

## 📌 개요
Account 템플릿의 공통 모듈입니다. 인증 관련 데이터 모델과 직렬화 스키마를 정의합니다.

## 🏗️ 구조
```
template/account/common/
├── account_model.py     # 데이터 모델 (빈 파일)
└── account_serialize.py # 요청/응답 직렬화 스키마
```

## 📊 account_serialize.py

### 회원가입 스키마
```python
class AccountSignupRequest(BaseRequest):
    id: str                      # 아이디 (필수)
    password: str               # 비밀번호 (필수)  
    name: Optional[str] = None  # 이름 (선택)
    phone: Optional[str] = None # 전화번호 (선택)

class AccountSignupResponse(BaseResponse):
    message: Optional[str] = None  # 성공시 access_token 반환
```

### 로그인 스키마  
```python
class AccountLoginRequest(BaseRequest):
    id: str       # 아이디
    password: str # 비밀번호

class AccountLoginResponse(BaseResponse):
    accessToken: str  # 세션 토큰
```

### 로그아웃 스키마
```python
class AccountLogoutRequest(BaseRequest):
    pass  # accessToken은 BaseRequest에서 상속

class AccountLogoutResponse(BaseResponse):
    pass  # 기본 응답만 사용
```

## 📝 account_model.py

**현재 상태**: 빈 파일
- 향후 Account 관련 도메인 모델 정의 예정
- 사용자 정보, 권한, 프로필 등의 데이터 클래스

## 💡 설계 특징

1. **BaseRequest/BaseResponse 상속**: 공통 프로토콜 준수
2. **Optional 필드**: 유연한 회원가입 정보 입력
3. **타입 힌팅**: 모든 필드에 명시적 타입 정의
4. **최소한의 구조**: 필요한 필드만 정의

이 모듈은 **인증 시스템의 계약**을 정의하는 **데이터 스키마 계층**입니다.