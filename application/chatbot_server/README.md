# Chatbot Server

## 📌 개요
Chatbot Server는 **메인 통합 마이크로서비스**입니다. 사용자 인증(Account)과 챗봇 서비스(Chatbot)를 제공하며, 다른 마이크로서비스들과 조율하는 허브 역할을 담당합니다.

## 🚀 실행 방법
```bash
python application/chatbot_server/main.py
```

## 🏗️ 구조
```
application/chatbot_server/
├── main.py              # FastAPI 서버 엔트리포인트
└── routers/
    ├── __init__.py
    ├── account.py       # 인증 API 라우터
    ├── chatbot.py       # 챗봇 API 라우터
    └── test.py          # 테스트 API 라우터
```

## ⚙️ 서버 설정

### 복합 템플릿 등록
```python
TemplateContext.add_template(TemplateType.ACCOUNT, AccountTemplateImpl())
TemplateContext.add_template(TemplateType.CHATBOT, ChatbotTemplateImpl())
```

### 인프라스트럭처 초기화

#### Redis 캐시 초기화
```python
cache_config = CacheConfig(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    session_expire_time=int(os.getenv("REDIS_SESSION_EXPIRE", 3600))
)
init_cache(cache_config)
```

#### 글로벌 DB 풀 초기화
```python
app.state.globaldb = MySQLPool()
await app.state.globaldb.init(
    host=os.getenv("DB_HOST", "localhost"),
    port=int(os.getenv("DB_PORT", 3306)),
    user=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASSWORD", ""),
    db=os.getenv("DB_NAME", "medichain_global")
)
```

#### 샤드 DB 풀 동적 초기화
```python
app.state.userdb_pools = {}
# 글로벌 DB에서 shard_info 테이블 조회
await cur.execute("SELECT shard_id, host, port, database_name, username, password FROM shard_info WHERE is_active=1")
for row in rows:
    shard_id, host, port, db_name, username, password = row
    pool = MySQLPool()
    await pool.init(host=host, port=port, user=username, password=password, db=db_name)
    app.state.userdb_pools[shard_id] = pool
```

#### HTTP 클라이언트 및 외부 서비스 설정
```python
app.state.http_client = HTTPClientPool()
app.state.category_server_url = os.getenv("CATEGORY_SERVER_URL", "http://localhost:8001")
```

## 🌐 CORS 미들웨어
```python
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 현재 모든 도메인 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 🔗 API 엔드포인트

### 라우터 구성
- **GET** `/` - 서버 상태 확인: `{"message": "Chatbot Server is running"}`
- **prefix** `/test`, **tags** `["test"]` - 테스트 API
- **prefix** `/account`, **tags** `["account"]` - 인증 API
- **prefix** `/chatbot`, **tags** `["chatbot"]` - 챗봇 API

## 🗄️ 사용되는 환경변수

### Redis 설정
- `REDIS_HOST` (기본값: "localhost")
- `REDIS_PORT` (기본값: 6379)
- `REDIS_SESSION_EXPIRE` (기본값: 3600)

### 글로벌 DB 설정
- `DB_HOST` (기본값: "localhost")
- `DB_PORT` (기본값: 3306)
- `DB_USER` (기본값: "root")
- `DB_PASSWORD` (기본값: "")
- `DB_NAME` (기본값: "medichain_global")

### 외부 서비스
- `CATEGORY_SERVER_URL` (기본값: "http://localhost:8001")
- `ALLOWED_ORIGINS` (기본값: "http://localhost:3000")

## 💡 실제 코드 특징

1. **복합 서비스**: Account + Chatbot 두 개의 템플릿 동시 운영
2. **인프라 허브**: Redis, MySQL(글로벌+샤드), HTTP 클라이언트 모든 서비스 초기화
3. **샤딩 지원**: `shard_info` 테이블 기반 동적 샤드 풀 생성
4. **마이크로서비스 조율**: Category Server와 HTTP 통신
5. **CORS 지원**: 프론트엔드와의 통신을 위한 CORS 설정
6. **에러 검증**: DB 풀 생성 실패 시 `RuntimeError` 발생

이 서버는 **API Gateway + 인증 서버 + 챗봇 서버**의 복합적인 역할을 담당하는 **메인 허브 서비스**입니다.