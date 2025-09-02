# Template Base Interface Module

## 📌 개요
Template Base Interface 모듈은 **도메인별 템플릿 인터페이스**를 정의합니다. 각 의료 도메인별로 BaseTemplate을 상속하는 추상 인터페이스를 제공하여 일관된 템플릿 구조를 보장합니다.

## 🏗️ 구조
```
template/base/template/
├── account_template.py          # 인증 템플릿 인터페이스
├── category_template.py         # 분류 템플릿 인터페이스
├── chatbot_template.py          # 챗봇 템플릿 인터페이스
├── clicnic_template.py          # 병원 템플릿 인터페이스 (오타: clinic)
├── drug_template.py             # 약품 템플릿 인터페이스
├── emergency_support_template.py # 응급지원 템플릿 인터페이스
└── internal_external.py         # 내외과 템플릿 인터페이스
```

## 💡 공통 패턴

### 기본 구조 (account_template.py 예시)
```python
from template.base.base_template import BaseTemplate

class AccountTemplate(BaseTemplate):
    def __init__(self):
        super().__init__()
        # Account 전용 초기화 코드가 있다면 여기에 작성

    # 필요한 경우 메서드 오버라이드
    # 예시 (빈 구현)
    # def some_account_method(self):
    #     pass
```

**특징**:
- `BaseTemplate` 상속
- `super().__init__()` 호출
- 도메인별 확장 포인트 제공
- 대부분 빈 구현체 (인터페이스 역할)

## 🎯 설계 목적

### 1. 계층적 상속 구조
```
BaseTemplate (추상 기반 클래스)
    ↓
AccountTemplate (도메인 인터페이스)
    ↓  
AccountTemplateImpl (실제 구현)
```

### 2. 도메인별 특화
각 템플릿 인터페이스는 해당 도메인의 특화된 메서드 정의 가능:
- `AccountTemplate`: 인증 관련 메서드
- `CategoryTemplate`: 분류 관련 메서드  
- `ChatbotTemplate`: 챗봇 관련 메서드
- 기타 도메인별 전용 메서드

### 3. 확장 포인트
- 도메인별 초기화 로직
- 도메인 특화 메서드 오버라이드
- 공통 BaseTemplate 메서드 재정의

## 🔗 실제 사용

### 구현체에서의 상속
```python
# template/account/account_template_impl.py
from template.base.template.account_template import AccountTemplate

class AccountTemplateImpl(AccountTemplate):
    # 실제 비즈니스 로직 구현
```

### 템플릿 등록
```python
# application/main.py
TemplateContext.add_template(TemplateType.ACCOUNT, AccountTemplateImpl())
```

## ⚠️ 현재 상태

**대부분 빈 구현**: 현재 대부분의 인터페이스 파일들이 빈 구현체로 되어 있음
- 기본 구조만 제공
- 주석으로 확장 포인트 안내
- 실제 도메인별 특화 메서드는 미구현

**파일명 오타**: `clicnic_template.py` (정확한 명칭: `clinic_template.py`)

## 💭 이 모듈의 역할

이 모듈은 **"계약(Contract)"**을 정의합니다:
- BaseTemplate의 공통 기능 상속
- 도메인별 확장 가능성 제공
- 일관된 템플릿 인터페이스 보장
- 구현체와 기반 클래스 사이의 중간 계층

**Interface Segregation Principle**을 따라 각 도메인이 필요한 인터페이스만 의존할 수 있도록 분리된 설계입니다.