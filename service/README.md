# Service Layer

## 📌 개요
Service Layer는 비즈니스 로직과 인프라스트럭처 사이의 추상화 계층입니다. 각 서비스는 특정 기술적 관심사를 담당하며, 상위 계층(application, template)에 일관된 인터페이스를 제공합니다.

## 🏗️ 전체 구조

```
service/
├── cache/        # Redis 기반 세션 및 캐싱
├── db/           # MySQL 연결 풀 관리
├── http/         # HTTP 클라이언트 풀
├── lang_chain/   # LLM 및 RAG 시스템
└── net/          # 프로토콜 기본 정의
```

## 🎯 왜 이렇게 구성했는가?

### 1. 기술적 관심사 분리
각 폴더는 **하나의 기술 스택**을 대표합니다:
- `cache/`: Redis 전문
- `db/`: MySQL 전문
- `http/`: HTTP 통신 전문
- `lang_chain/`: AI/LLM 전문
- `net/`: 프로토콜 정의

### 2. 계층적 의존성

```
application (FastAPI 서버들)
    ↓
template (비즈니스 로직)
    ↓
service (기술 서비스)
    ↓
외부 시스템 (Redis, MySQL, OpenAI)
```

### 3. 플러그인 아키텍처
각 서비스는 독립적으로 초기화되고 주입됩니다:
```python
# main.py의 lifespan에서
init_cache(cache_config)        # cache 서비스
app.state.globaldb = MySQLPool() # db 서비스
app.state.http_client = HTTPClientPool() # http 서비스
```

## 💡 서비스 간 관계

### 1. 독립적인 서비스들
```
cache ← 세션 관리
  ↕ (독립)
db ← 영구 저장소
  ↕ (독립)
http ← 외부 통신
  ↕ (독립)
lang_chain ← AI 처리
```

### 2. 협력 패턴
- **cache + db**: 캐시 미스 시 DB 조회
- **http + lang_chain**: OpenAI API 호출
- **net + 모든 서비스**: 공통 프로토콜 사용

## 🔄 실제 데이터 플로우

```
1. 요청 수신 (application)
    ↓
2. 세션 검증 (cache/dependencies.py)
    ↓
3. 비즈니스 로직 (template)
    ↓
4. 데이터 조회 (db) / AI 처리 (lang_chain)
    ↓
5. 외부 API 호출 (http) - 필요시
    ↓
6. 응답 반환 (net/protocol_base)
```

## 📊 각 서비스의 핵심 역할

### cache/ (상태 관리)
- **기술**: Redis, async/await
- **역할**: 세션, 임시 데이터
- **특징**: TTL 기반 자동 만료

### db/ (영구 저장)
- **기술**: aiomysql, 연결 풀
- **역할**: 데이터 CRUD
- **특징**: 샤딩 지원

### http/ (외부 통신)
- **기술**: httpx, 비동기
- **역할**: 마이크로서비스 간 통신
- **특징**: 연결 재사용

### lang_chain/ (AI 처리)
- **기술**: LangChain, FAISS, OpenAI
- **역할**: RAG 기반 응답 생성
- **특징**: 도메인별 특화

### net/ (프로토콜)
- **기술**: Pydantic
- **역할**: 요청/응답 표준화
- **특징**: 타입 안정성

## 🚀 초기화 순서

```python
# main.py lifespan에서 실제 초기화 순서
1. 템플릿 등록 (TemplateContext)
2. Redis 초기화 (init_cache)
3. DB 풀 생성 (MySQLPool)
4. HTTP 클라이언트 생성 (HTTPClientPool)
5. LangChain 모델 로드 (각 템플릿에서)
```

## 🎓 설계 원칙

### 1. 의존성 역전 (DIP)
상위 계층이 추상화에 의존:
```python
# template은 구체적인 Redis가 아닌 
# cache 서비스의 인터페이스에 의존
```

### 2. 단일 책임 (SRP)
각 서비스는 하나의 기술적 책임:
- cache는 캐싱만
- db는 데이터베이스만
- http는 HTTP 통신만

### 3. 개방-폐쇄 (OCP)
새 서비스 추가 시 기존 코드 수정 불필요:
```python
# 새로운 서비스 추가 예시
service/
└── message_queue/  # 새 서비스 추가
```

## ⚠️ 실제 코드의 특징

### 강점
1. **명확한 경계**: 각 서비스의 역할이 분명
2. **비동기 일관성**: 모든 서비스가 async/await
3. **타입 안정성**: Pydantic 모델 활용

### 개선 가능 영역
1. **중복 코드**: lang_chain의 emergency와 internal_external
2. **에러 처리**: 일부 서비스에 에러 처리 부재
3. **인터페이스 부재**: 추상 클래스/프로토콜 미정의

## 🔗 상위 계층과의 연결

### application → service
```python
# main.py에서 서비스 초기화
app.state.globaldb = MySQLPool()
app.state.http_client = HTTPClientPool()
```

### template → service
```python
# 템플릿에서 서비스 사용
from service.cache.async_session import get_session_info
from service.db.database import MySQLPool
```

## 💭 이 구조의 의미

Service Layer는 **"기술과 비즈니스의 분리"**를 실현합니다:
- 비즈니스 로직은 기술 세부사항을 몰라도 됨
- 기술 스택 변경 시 서비스 계층만 수정
- 테스트 시 서비스 계층을 모킹 가능

이는 **클린 아키텍처**의 핵심 원칙을 따르는 설계입니다.