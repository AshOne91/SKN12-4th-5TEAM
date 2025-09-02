# Application Layer

## 📌 개요
Application Layer는 **마이크로서비스 아키텍처의 진입점**으로, 각 의료 도메인별 독립적인 FastAPI 서버를 제공합니다. HTTP 요청을 받아 해당 도메인의 템플릿으로 라우팅하는 역할을 담당합니다.

## 🏗️ 마이크로서비스 구조

```
application/
├── chatbot_server/         # 메인 서버 (통합 서비스)
│   ├── main.py            # 복합 서비스 (account + chatbot)
│   └── routers/
│       ├── account.py     # 인증 API
│       ├── chatbot.py     # 챗봇 API  
│       └── test.py        # 테스트 API
├── category_server/        # 증상 분류 전용 서버
│   ├── main.py
│   └── routers/
│       └── category.py
├── clinic_server/          # 병원 정보 전용 서버
│   ├── main.py
│   └── routers/
│       └── clinic.py
├── drug_server/           # 약품 정보 전용 서버
│   ├── main.py
│   └── routers/
│       └── drug.py
├── emergency_support_server/ # 응급 지원 전용 서버
│   ├── main.py
│   └── routers/
│       └── emergency_support.py
└── internal_external_server/ # 내외과 구분 전용 서버
    ├── main.py
    └── routers/
        └── internal_external.py
```

## 🎯 왜 마이크로서비스로 분리했는가?

### 1. 도메인별 독립 배포
```python
# 각 서버는 독립적으로 실행 가능
python application/category_server/main.py    # 포트 8001
python application/clinic_server/main.py      # 포트 8002  
python application/drug_server/main.py        # 포트 8003
```
**이점**: 특정 도메인 수정 시 전체 시스템 재배포 불필요

### 2. 확장성
- **수평 확장**: 부하가 높은 서비스만 인스턴스 증가
- **리소스 최적화**: 각 서비스별 필요 리소스만 할당
- **장애 격리**: 한 서비스 장애가 다른 서비스에 영향 없음

### 3. 기술적 다양성
각 서비스는 도메인 특성에 맞는 기술 스택 선택 가능:
- `category_server`: 분류 AI 특화
- `drug_server`: 약품 검색 최적화
- `emergency_support_server`: 실시간 응답 최적화

## 💡 서버별 역할 분석

### chatbot_server (메인 허브)
```python
# 가장 복잡한 서버 - 여러 템플릿 통합
TemplateContext.add_template(TemplateType.ACCOUNT, AccountTemplateImpl())
TemplateContext.add_template(TemplateType.CHATBOT, ChatbotTemplateImpl())

# 다양한 서비스 의존
app.state.globaldb = MySQLPool()      # 글로벌 DB
app.state.userdb_pools = {...}        # 샤드 DB들
app.state.http_client = HTTPClientPool()  # 다른 서버와 통신
app.state.category_server_url = "..."     # 카테고리 서버 URL
```
**역할**: 
- 사용자 인증 (account)
- 통합 챗봇 서비스 (chatbot)
- 다른 마이크로서비스와 조율

### category_server (분류 전용)
```python
# 단순한 서버 - 카테고리 템플릿만
TemplateContext.add_template(TemplateType.CATEGORY, CategoryTemplateImpl())

@router.post("/ask")
async def category_ask(request: CategoryAskRequest):
    # 질문을 받아 적절한 의료 분야 분류
```
**역할**: 의료 질문의 도메인 분류만 담당

### clinic_server (병원 정보)
```python
# 명시적 초기화
clinic_template_instance = ClinicTemplateImpl()
clinic_template_instance.init(config=None)
TemplateContext.add_template(TemplateType.CLINIC, clinic_template_instance)
```
**역할**: 병원/의료기관 정보 제공

### 기타 전용 서버들
- `drug_server`: 약품 정보 전용
- `emergency_support_server`: 응급 상황 전용  
- `internal_external_server`: 내과/외과 구분 전용

## 🔄 서비스 간 통신 패턴

### 1. chatbot_server → category_server
```python
# chatbot_template_impl.py에서
category_req = CategoryAskRequest(question=message)
resp = await http_client.post(
    f"{category_server_url}/category/ask",
    json=category_req.model_dump()
)
```

### 2. API Gateway 패턴 (부분적)
`chatbot_server`가 일종의 API Gateway 역할:
- 인증 처리 (account)
- 다른 서비스 조율 (category_server 호출)
- 통합 응답 생성 (chatbot)

### 3. 독립적 서비스
나머지 서버들은 독립적으로 동작:
```python
# 각 서버의 단순한 패턴
@router.post("/endpoint")
async def handle_request(request: DomainRequest):
    template = TemplateContext.get_template(TemplateType.DOMAIN)
    return await template.on_domain_req(request)
```

## ⚙️ 공통 아키텍처 패턴

### 1. FastAPI + lifespan 패턴
```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 서버 시작 시 템플릿 등록
    TemplateContext.add_template(TemplateType.X, XTemplateImpl())
    yield
    # 서버 종료 시 정리 (필요한 경우)

app = FastAPI(lifespan=lifespan)
```

### 2. 라우터 기반 모듈화
```python
# 각 서버는 도메인별 라우터 사용
app.include_router(domain.router, prefix="/domain", tags=["domain"])
```

### 3. 템플릿 위임 패턴
```python
# 모든 라우터는 비즈니스 로직을 템플릿에 위임
@router.post("/endpoint")
async def endpoint(request: Request):
    template = TemplateContext.get_template(TemplateType.DOMAIN)
    return await template.on_domain_req(request)
```

## 🌐 네트워크 구성

### 포트 분배 (예상)
- `chatbot_server`: 8000 (메인)
- `category_server`: 8001  
- `clinic_server`: 8002
- `drug_server`: 8003
- `emergency_support_server`: 8004
- `internal_external_server`: 8005

### 로드 밸런서 구성 (배포 시)
```
Load Balancer
├── chatbot_server (메인 트래픽)
├── category_server (분류 요청)
├── drug_server (약품 검색)
└── emergency_support_server (응급 상황)
```

## 📊 리소스 사용량 분석

### chatbot_server (고사양)
- **CPU**: 높음 (AI 처리, 다중 서비스 조율)
- **메모리**: 높음 (여러 템플릿, 연결 풀)
- **네트워크**: 높음 (다른 서비스와 통신)

### 전용 서버들 (경량)
- **CPU**: 낮음-보통 (단일 도메인 처리)
- **메모리**: 낮음 (단일 템플릿)
- **네트워크**: 낮음 (독립적 동작)

## 🔧 배포 및 운영

### 1. 컨테이너화 (Docker)
```dockerfile
# 각 서버별 독립 컨테이너
FROM python:3.11
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "application/chatbot_server/main.py"]
```

### 2. 서비스 메시 (Kubernetes)
```yaml
apiVersion: v1
kind: Service
metadata:
  name: category-service
spec:
  selector:
    app: category-server
  ports:
    - port: 8001
```

### 3. 모니터링
- **헬스체크**: 각 서버의 `/` 엔드포인트
- **메트릭**: 서비스별 응답 시간, 에러율
- **로그**: 중앙 집중식 로그 수집

## ⚠️ 실제 코드의 특징

### 강점
1. **명확한 분리**: 각 서버의 역할이 분명
2. **템플릿 통합**: 모든 서버가 동일한 템플릿 시스템 사용
3. **경량 구조**: 불필요한 의존성 없는 깔끔한 구조

### 개선 가능 영역
1. **초기화 불일치**: clinic_server만 명시적 init() 호출
2. **에러 처리**: 공통 에러 처리 미들웨어 부재
3. **설정 관리**: 서버별 설정 파일 표준화 필요

## 🎓 이 계층에서 배울 수 있는 것

1. **마이크로서비스 아키텍처**: 도메인별 서비스 분리
2. **FastAPI 고급**: lifespan, 라우터, 미들웨어
3. **서비스 메시**: 서비스 간 통신과 조율
4. **확장성 설계**: 수평 확장과 로드 밸런싱
5. **운영 관점**: 배포, 모니터링, 유지보수

## 💭 설계 철학

Application Layer는 **"단일 책임의 집합"**입니다:
- 각 서버는 하나의 도메인만 담당
- chatbot_server는 조율자 역할
- 비즈니스 로직은 template에 위임
- HTTP 처리만 집중

이는 **Conway's Law**를 반영한 설계로, "시스템 구조는 조직 구조를 반영한다"는 원칙에 따라 의료 전문 분야별로 서비스를 분리했습니다.

Application Layer는 **의료 서비스의 관문**으로서, 클라이언트의 요청을 적절한 전문 영역으로 라우팅하는 핵심 역할을 담당합니다.