# Template Layer

## 📌 개요
Template Layer는 **비즈니스 로직의 핵심**을 담당하는 계층입니다. 각 의료 도메인별 전문 로직을 플러그인 방식으로 관리하며, 확장 가능한 아키텍처를 제공합니다.

## 🏗️ 전체 구조

```
template/
├── base/           # 템플릿 시스템 기반
│   ├── base_template.py      # 추상 기반 클래스
│   ├── template_context.py   # 템플릿 관리자
│   ├── template_type.py      # 도메인 타입 정의
│   ├── session_info.py       # 세션 모델
│   └── template/             # 인터페이스 정의
├── account/        # 인증/계정 관리
├── chatbot/        # 의료 상담 챗봇
├── category/       # 증상 분류
├── clinic/         # 병원 정보
├── drug/          # 약품 정보
├── emergency_support/   # 응급 지원
└── internal_external/  # 내과/외과 구분
```

## 🎯 왜 이런 구조인가?

### 1. 도메인 주도 설계 (DDD)
각 폴더는 **의료 분야의 실제 전문 영역**을 반영:
- `account`: 환자 인증 시스템
- `chatbot`: 의료 상담 AI
- `category`: 증상별 분류 전문가
- `clinic`: 병원/의료진 정보
- `drug`: 약품/처방 전문가
- `emergency_support`: 응급 상황 대응
- `internal_external`: 내과/외과 구분

### 2. 플러그인 아키텍처
```python
# 새로운 도메인 추가 시
1. template/[domain]/ 폴더 생성
2. [Domain]TemplateImpl 클래스 구현
3. TemplateType에 새 타입 추가
4. main.py에서 등록
```

### 3. 관심사의 분리
```
비즈니스 로직 (template) ←→ 기술 구현 (service)
   ↑                           ↑
도메인 전문성                기술 전문성
```

## 💡 핵심 설계 패턴

### 1. Template Method Pattern
```python
class BaseTemplate(ABC):
    def init(self, config):         # 초기화 훅
    def on_load_data(self, config): # 데이터 로딩 훅
    def on_client_create(...):      # 클라이언트 생성 훅
    def on_client_update(...):      # 클라이언트 업데이트 훅
    def on_client_delete(...):      # 클라이언트 삭제 훅
```
**의도**: 모든 도메인이 동일한 라이프사이클 보장

### 2. Registry Pattern
```python
class TemplateContext:
    _templates = {}  # 도메인별 템플릿 저장소
    
    @classmethod
    def add_template(cls, key: TemplateType, value):
        # 런타임에 템플릿 등록
    
    @classmethod  
    def get_template(cls, key: TemplateType):
        # 타입 안전한 템플릿 조회
```
**효과**: 동적 모듈 관리 + 타입 안전성

### 3. Strategy Pattern
각 도메인은 **동일한 문제에 대한 다른 해결 전략**:
- 모두 "사용자 질문에 응답"하지만
- 각자 다른 전문 지식과 처리 방식

## 🔄 실제 동작 플로우

### 1. 시스템 초기화
```python
# main.py lifespan에서
TemplateContext.add_template(TemplateType.ACCOUNT, AccountTemplateImpl())
TemplateContext.add_template(TemplateType.CHATBOT, ChatbotTemplateImpl())
# ... 각 도메인별 템플릿 등록

TemplateContext.init_template(config)       # 모든 템플릿 초기화
TemplateContext.load_data_table(config)     # 모든 템플릿 데이터 로딩
```

### 2. 요청 처리
```python
# application/routers에서
template = TemplateContext.get_template(TemplateType.CHATBOT)
response = await template.on_chatbot_message_req(...)
```

### 3. 라이프사이클 이벤트
```python
# 클라이언트 생성/수정/삭제 시 모든 템플릿에 알림
TemplateContext.create_client(db_client, session)
TemplateContext.update_client(db_client, session)  
TemplateContext.delete_client(db_client, user_id)
```

## 📊 도메인별 특징 분석

### account (인증/보안)
- **기술**: SHA256+Salt, UUID 토큰, 샤딩
- **특징**: 보안 중심, 사용자별 샤드 할당
- **핵심**: 안전한 인증 및 세션 관리

### chatbot (의료 상담)
- **기술**: 다단계 AI 파이프라인, Redis 히스토리
- **특징**: 카테고리 서버 → 최종 LLM 2단계 처리
- **핵심**: 컨텍스트 기반 대화형 AI

### category (증상 분류)
- **기술**: 벡터 검색, 분류 AI
- **특징**: 질문을 적절한 의료 분야로 라우팅
- **핵심**: 의료 도메인 분류 전문가

### clinic (병원 정보)
- **기술**: 지역별 검색, 의료진 정보
- **특징**: 위치 기반 병원 추천
- **핵심**: 의료 기관 정보 서비스

### drug (약품 정보)
- **기술**: RAG, 약품 데이터베이스
- **특징**: 처방전/복용법 전문 상담
- **핵심**: 약물 정보 전문가

### emergency_support (응급 지원)
- **기술**: 긴급 상황 판단, 응급 처치 가이드
- **특징**: 실시간 응급 상황 대응
- **핵심**: 응급 의료 지원 시스템

### internal_external (내외과)
- **기술**: 내과/외과 구분 AI
- **특징**: 증상별 적절한 과 추천
- **핵심**: 의료 과목 전문 상담

## 🗄️ 데이터 관리 전략

### 1. 계층별 데이터 분리
```
글로벌 DB (Global)
├── users (사용자 기본 정보)
├── user_shard_mapping (샤드 매핑)
└── shard_info (샤드 서버 정보)

샤드 DB (Per User)
├── chat_room (채팅방)
├── user_profile (사용자 프로필)  
└── medical_history (진료 기록)

Redis (Cache)
├── sessions (세션 정보)
└── chat_history (대화 내역)
```

### 2. 도메인별 데이터 모델
각 템플릿은 **고유한 데이터 구조**를 가짐:
- `account`: 인증 정보, 세션 상태
- `chatbot`: 채팅방, 메시지 히스토리
- `drug`: 약품 정보, 상호작용 데이터

## 🤖 AI 통합 전략

### 1. service/lang_chain 활용
각 템플릿은 도메인별 LangChain 모듈 사용:
```python
from service.lang_chain.drug_lang_chain import Vector_store
from service.lang_chain.category_classifer import Category_Classifier
```

### 2. 다단계 AI 처리
```
사용자 질문
    ↓
category (질문 분류)
    ↓  
해당 도메인 template (전문 처리)
    ↓
chatbot (최종 통합 응답)
```

## 🔐 세션 및 보안

### SessionInfo 중앙 관리
```python
@dataclass
class SessionInfo:
    user_id: str
    platform_id: str  
    account_id: str
    session_state: ClientSessionState
    shard_id: int  # 샤딩 지원
```

### 상태 기반 세션 관리
```python
class ClientSessionState(Enum):
    NONE = "None"           # 정상
    FATAL = "Fatal"         # 치명적 오류
    EXPIRED = "Expired"     # 만료
    DUPLICATED = "Duplicated"  # 중복 로그인
    BLOCKED = "Blocked"     # 차단
    NETERROR = "NetError"   # 네트워크 오류
```

## 📈 확장성 설계

### 1. 새로운 도메인 추가
```python
# 1. 새 TemplateType 정의
class TemplateType(Enum):
    NEW_DOMAIN = auto()

# 2. 구현체 작성
class NewDomainTemplateImpl(BaseTemplate):
    async def on_new_domain_request(self, ...):
        pass

# 3. 등록
TemplateContext.add_template(TemplateType.NEW_DOMAIN, NewDomainTemplateImpl())
```

### 2. 샤딩 지원
- 사용자별 데이터는 샤드 DB에 분산
- 글로벌 정보는 중앙 DB에서 관리
- 동적 샤드 추가/제거 가능

## ⚠️ 실제 코드의 특징

### 강점
1. **명확한 도메인 분리**: 의료 전문 분야별 모듈화
2. **플러그인 아키텍처**: 새 도메인 추가 용이
3. **타입 안전성**: TemplateType enum 활용
4. **라이프사이클 관리**: 일관된 초기화/정리 패턴

### 개선 가능 영역
1. **중복 코드**: base/cache_config.py와 service/cache/cache_config.py 중복
2. **빈 인터페이스**: 대부분의 base/template/ 파일들이 빈 구현
3. **에러 처리**: 일관되지 않은 에러 코드 관리

## 🔗 다른 계층과의 관계

### template → service (의존)
```python
from service.cache.async_session import get_session_info
from service.db.database import MySQLPool  
from service.lang_chain.drug_lang_chain import Vector_store
```

### application → template (사용)
```python
template = TemplateContext.get_template(TemplateType.ACCOUNT)
response = await template.on_account_login_req(...)
```

## 🎓 이 계층에서 배울 수 있는 것

1. **도메인 주도 설계**: 비즈니스 도메인의 소프트웨어 반영
2. **플러그인 아키텍처**: 확장 가능한 모듈 설계
3. **의료 AI 시스템**: 전문 분야별 AI 활용
4. **샤딩 실전**: 대규모 사용자 데이터 분할
5. **세션 관리**: 상태 기반 사용자 세션 처리

## 💭 설계 철학

Template Layer는 **"도메인의 언어로 코드를 작성"**합니다:
- `account.login()` - 개발자가 아닌 의료진도 이해 가능
- `chatbot.ask_medical_question()` - 비즈니스 의도가 명확
- `emergency.handle_urgent_case()` - 도메인 전문성 반영

이는 **유비쿼터스 언어(Ubiquitous Language)** 원칙을 따른 설계로, 기술팀과 의료진이 동일한 언어로 소통할 수 있게 합니다.

Template Layer는 **의료 서비스의 두뇌**로서, 각 전문 분야의 지식을 코드로 구현한 핵심 계층입니다.