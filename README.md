# FastAPI Base Server

C# 기반 서버 구조를 FastAPI로 변환한 프로젝트입니다.

## 구조

### C# vs FastAPI 비교

| C# | FastAPI |
|---|---|
| `TemplateStartup.Run()` | `lifespan` 이벤트 핸들러 |
| `ServerParameter` | `ServerParameter` 클래스 |
| `AppConfig` | `AppConfig` 클래스 |
| `GameBaseTemplateContext` | `TemplateContext` |
| `ETemplateType` | `TemplateType` Enum |

## 주요 기능

### 1. 앱 시작 시 초기화
- 로거 설정
- 템플릿 등록 및 초기화
- 서비스 초기화 (데이터베이스, 캐시, 이벤트, 메시지큐, 빌링)
- 설정 파일 로딩

### 2. 템플릿 시스템
- `BaseTemplate`: 모든 템플릿의 기본 클래스
- `TemplateContext`: 템플릿 관리 및 라이프사이클 관리
- 각 도메인별 템플릿 구현체

### 3. 설정 관리
- 환경별 설정 파일 (`config.json`, `config_debug.json`)
- JSON 기반 설정 로딩
- 기본값 폴백 지원

## 설치 및 실행

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. 설정 파일 준비
- `config.json` 또는 `config_debug.json` 파일을 프로젝트 루트에 배치
- 환경 변수 `DEBUG=true`로 설정하면 디버그 설정 파일 사용

### 3. 서버 실행
```bash
# 개발 모드
DEBUG=true python application/chatbot_server/main.py

# 프로덕션 모드
python application/chatbot_server/main.py
```

또는 uvicorn 직접 사용:
```bash
uvicorn application.chatbot_server.main:app --host 0.0.0.0 --port 8000 --reload
```

## API 엔드포인트

- `GET /`: 서버 상태 확인
- `GET /health`: 헬스 체크
- `GET /docs`: Swagger UI (FastAPI 자동 생성)

## 템플릿 추가 방법

1. `template/base/template_type.py`에 새로운 템플릿 타입 추가
2. `template/[domain]/[domain]_template_impl.py` 생성
3. `BaseTemplate` 상속하여 구현
4. `main.py`의 `TemplateStartup.run()`에서 템플릿 등록

## 서비스 구현

현재 주석 처리된 서비스들을 실제 구현하려면:

1. `service/` 디렉토리에 각 서비스 모듈 생성
2. `main.py`에서 주석 해제
3. 해당 서비스의 초기화 로직 구현

## 설정 파일 구조

```json
{
  "databaseConfig": {
    "firestoreProductId": "project-id",
    "firestorePrivateKey": "private-key",
    "tables": {}
  },
  "cacheConfig": {
    "host": "localhost",
    "port": 6379,
    "sessionExpireTime": 3600
  },
  "eventConfig": {
    "enabled": true,
    "eventQueue": "events"
  },
  "messageQueueConfig": {
    "host": "localhost",
    "port": 5672,
    "username": "guest",
    "password": "guest"
  },
  "billingConfig": {
    "enabled": false,
    "provider": "none"
  },
  "templateConfig": {
    "gameId": "fastapi-base-server",
    "env": "development"
  }
}
``` 