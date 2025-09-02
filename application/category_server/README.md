# Category Server

## 📌 개요
Category Server는 **의료 질문 분류 전용 마이크로서비스**입니다. 사용자 질문을 적절한 의료 도메인으로 분류하고, 해당 도메인의 전용 서버로 라우팅하는 역할을 담당합니다.

## 🚀 실행 방법
```bash
python application/category_server/main.py
```

## 🏗️ 구조
```
application/category_server/
├── main.py              # FastAPI 서버 엔트리포인트
└── routers/
    ├── __init__.py
    └── category.py      # 분류 API 라우터
```

## ⚙️ 서버 설정

### FastAPI 애플리케이션
```python
app = FastAPI(lifespan=lifespan)
app.include_router(category.router, prefix="/category", tags=["category"])
```

### 템플릿 등록
```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    TemplateContext.add_template(TemplateType.CATEGORY, CategoryTemplateImpl())
    yield
```

## 🔗 API 엔드포인트

### 루트 엔드포인트
- **GET** `/` - 서버 상태 확인
- **응답**: `{"message": "Category Server is running"}`

### 카테고리 분류 API
- **접두사**: `/category`
- **태그**: `["category"]`
- **라우터**: `category.router`

## 💡 실제 코드 특징

1. **단일 템플릿**: `CategoryTemplateImpl`만 등록하는 단순한 구조
2. **마이크로서비스**: 분류 기능만 담당하는 전용 서비스
3. **독립 실행**: 다른 서버와 독립적으로 실행 가능
4. **템플릿 시스템**: 공통 템플릿 컨텍스트 시스템 사용

이 서버는 **의료 질문 라우터**로서 전체 의료 상담 시스템의 **트래픽 제어 허브** 역할을 담당합니다.