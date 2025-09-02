# Template Base Module

## 📌 모듈 개요
Template Base 모듈은 전체 템플릿 시스템의 **기반 구조**를 정의합니다. 도메인별 비즈니스 로직을 플러그인 방식으로 관리할 수 있는 아키텍처를 제공합니다.

## 🏗️ 실제 구조 분석

```
template/base/
├── base_template.py      # 추상 기반 클래스
├── template_context.py   # 템플릿 관리자 (싱글톤)
├── template_type.py      # 도메인 타입 열거형
├── session_info.py       # 세션 모델 정의
├── template_config.py    # 설정 통합 모델
├── cache_config.py       # 캐시 설정 (중복)
└── template/             # 도메인별 인터페이스
    ├── account_template.py
    ├── category_template.py
    ├── chatbot_template.py
    ├── clicnic_template.py
    ├── drug_template.py
    ├── emergency_support_template.py
    └── internal_external.py
```

## 🎯 핵심 설계 패턴

### 1. Template Method Pattern (BaseTemplate)
```python
class BaseTemplate(ABC):
    def init(self, config):         # 초기화
    def on_load_data(self, config): # 데이터 로딩
    def on_client_create(...):      # 클라이언트 생성 이벤트
    def on_client_update(...):      # 클라이언트 업데이트 이벤트
    def on_client_delete(...):      # 클라이언트 삭제 이벤트
```
**의도**: 모든 템플릿이 동일한 라이프사이클을 갖도록 강제

### 2. Registry Pattern (TemplateContext)
```python
class TemplateContext:
    _templates = {}  # 등록된 템플릿 저장소
    _lock = Lock()   # 스레드 안전성
    
    @classmethod
    def add_template(cls, key: TemplateType, value):
        # 템플릿 등록
    
    @classmethod
    def get_template(cls, key: TemplateType):
        # 템플릿 조회
```
**특징**: 
- 싱글톤 패턴으로 전역 관리
- 스레드 안전성을 위한 Lock 사용
- 타입 안전성을 위한 TemplateType 사용

### 3. Strategy Pattern (도메인별 템플릿)
```python
class TemplateType(Enum):
    ACCOUNT = auto()
    CHATBOT = auto()
    CATEGORY = auto()
    CLINIC = auto()
    DRUG = auto()
    EMERGENCY_SUPPORT = auto()
    INTERNAL_EXTERNAL = auto()
```
**의도**: 각 도메인별로 다른 비즈니스 로직 전략

## 🔄 템플릿 라이프사이클

```python
# 1. 등록 (main.py에서)
TemplateContext.add_template(TemplateType.CHATBOT, ChatbotTemplateImpl())

# 2. 초기화
TemplateContext.init_template(config)

# 3. 데이터 로딩
TemplateContext.load_data_table(config)

# 4. 클라이언트 이벤트 처리
TemplateContext.create_client(db_client, session)
TemplateContext.update_client(db_client, session)
TemplateContext.delete_client(db_client, user_id)
```

## 🧩 세션 관리 시스템

### SessionInfo 데이터 구조
```python
@dataclass
class SessionInfo:
    user_id: str = ""           # 사용자 ID
    platform_id: str = ""      # 플랫폼 식별자
    platform_type: int = -1    # 플랫폼 타입
    account_id: str = ""        # 계정 ID
    account_level: int = 0      # 계정 레벨
    app_version: str = ""       # 앱 버전
    os: str = ""               # 운영체제
    country: str = ""          # 국가
    session_state: ClientSessionState = ClientSessionState.NONE
    shard_id: int = -1         # 샤드 ID
```

### 세션 상태 관리
```python
class ClientSessionState(str, Enum):
    NONE = "None"           # 정상 상태
    FATAL = "Fatal"         # 치명적 오류
    EXPIRED = "Expired"     # 세션 만료
    DUPLICATED = "Duplicated"  # 중복 로그인
    BLOCKED = "Blocked"     # 차단된 계정
    NETERROR = "NetError"   # 네트워크 오류
```

## ⚙️ 설정 통합 시스템

### AppConfig 구조
```python
class AppConfig(BaseModel):
    template_config: TemplateConfig    # 템플릿 설정
    database_config: DatabaseConfig    # DB 설정
    cache_config: CacheConfig         # 캐시 설정
```

### TemplateConfig 내용
```python
class TemplateConfig(BaseModel):
    app_id: str = ""                    # 앱 식별자
    env: str = ""                       # 환경 (dev/prod)
    local_path: str = ""                # 로컬 파일 경로
    bucket_env: str = ""                # S3 버킷 환경
    bucket_url: str = ""                # S3 URL
    bucket_name: str = ""               # S3 버킷명
    aws_access_key_id: str = ""         # AWS 액세스 키
    aws_secret_access_key: str = ""     # AWS 시크릿 키
```

## 🔗 실제 사용 패턴

### 1. 템플릿 등록 (main.py)
```python
# 실제 코드에서 사용
TemplateContext.add_template(TemplateType.ACCOUNT, AccountTemplateImpl())
TemplateContext.add_template(TemplateType.CHATBOT, ChatbotTemplateImpl())
```

### 2. 일괄 처리
```python
# 모든 템플릿의 메서드를 한 번에 호출
for t in cls._templates.values():
    t.init(config)              # 모든 템플릿 초기화
    t.on_load_data(config)      # 모든 템플릿 데이터 로딩
```

### 3. 스레드 안전성
```python
with cls._lock:
    if key in cls._templates:
        return False
    cls._templates[key] = value  # 경쟁 조건 방지
```

## 📊 실제 템플릿 인터페이스 현황

### template/ 폴더의 인터페이스들
- `account_template.py`: 빈 구현체 (BaseTemplate만 상속)
- `category_template.py`: 카테고리 관리 인터페이스
- `chatbot_template.py`: 챗봇 로직 인터페이스  
- `clicnic_template.py`: 병원 정보 인터페이스
- `drug_template.py`: 약품 정보 인터페이스
- `emergency_support_template.py`: 응급 지원 인터페이스
- `internal_external.py`: 내과/외과 인터페이스

## ⚠️ 코드에서 발견된 이슈

### 1. 중복 코드
- `template/base/cache_config.py`와 `service/cache/cache_config.py` 동일

### 2. 빈 인터페이스
- 대부분의 template/ 인터페이스가 빈 구현

### 3. 명명 불일치
- `clicnic_template.py` (오타: clinic이 맞음)

## 🎓 이 모듈에서 배울 수 있는 것

1. **플러그인 아키텍처**: 동적 모듈 등록과 관리
2. **라이프사이클 관리**: 일관된 초기화/정리 패턴
3. **스레드 안전성**: 멀티스레딩 환경에서의 안전한 공유 자원 관리
4. **타입 안전성**: Enum을 활용한 컴파일 타임 검증
5. **설정 통합**: 여러 서비스 설정의 중앙 집중화

## 💭 설계 철학

이 모듈은 **"확장성과 일관성"**을 동시에 추구합니다:
- 새로운 도메인 추가 시 기존 코드 수정 없이 확장
- 모든 도메인이 동일한 패턴과 라이프사이클 준수
- 중앙 집중적 관리를 통한 복잡성 감소

**Template Method + Registry + Strategy** 패턴의 조합으로 유연하면서도 일관된 아키텍처를 구현했습니다.