# Emergency Support Server Routers

## 📌 개요
Emergency Support Server의 API 라우터 모듈입니다. 응급 의료 지원 관련 HTTP 엔드포인트를 제공합니다.

## 🏗️ 구조
```
application/emergency_support_server/routers/
├── __init__.py
└── emergency_support.py    # 응급 지원 API 라우터
```

## 🔗 API 엔드포인트

### emergency_support.py

응급 의료 지원 RAG 시스템 관련 API를 제공합니다.

**공통 패턴**:
- 템플릿 조회: `TemplateContext.get_template(TemplateType.EMERGENCY_SUPPORT)`
- 템플릿 검증: 미등록 시 `RuntimeError` 발생
- 비즈니스 로직 위임: `emergency_template.on_emergency_support_ask_req()` 호출

이 라우터는 **응급 의료 전문 API**를 제공하는 **생명 구조 HTTP 브리지**입니다.