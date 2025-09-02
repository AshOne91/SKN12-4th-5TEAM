# Internal External Server Routers

## 📌 개요
Internal External Server의 API 라우터 모듈입니다. 내과/외과 구분 관련 HTTP 엔드포인트를 제공합니다.

## 🏗️ 구조
```
application/internal_external_server/routers/
├── __init__.py
└── internal_external.py    # 내과/외과 구분 API 라우터
```

## 🔗 API 엔드포인트

### internal_external.py

내과/외과 구분 RAG 시스템 관련 API를 제공합니다.

**공통 패턴**:
- 템플릿 조회: `TemplateContext.get_template(TemplateType.INTERNAL_EXTERNAL)`
- 템플릿 검증: 미등록 시 `RuntimeError` 발생
- 비즈니스 로직 위임: `internal_external_template.on_internal_external_ask_req()` 호출

이 라우터는 **내과/외과 전문 API**를 제공하는 **진료과 라우팅 HTTP 브리지**입니다.