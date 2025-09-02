# Clinic Server Routers

## 📌 개요
Clinic Server의 API 라우터 모듈입니다. 병원 및 의료진 정보 관련 HTTP 엔드포인트를 제공합니다.

## 🏗️ 구조
```
application/clinic_server/routers/
├── __init__.py
└── clinic.py        # 병원 정보 API 라우터
```

## 🔗 API 엔드포인트

### clinic.py

병원 정보 RAG 시스템 관련 API를 제공합니다.

**공통 패턴**:
- 템플릿 조회: `TemplateContext.get_template(TemplateType.CLINIC)`
- 템플릿 검증: 미등록 시 `RuntimeError` 발생
- 비즈니스 로직 위임: `clinic_template.on_clinic_ask_req()` 호출

이 라우터는 **병원 정보 전문 API**를 제공하는 **HTTP ↔ 템플릿 브리지**입니다.