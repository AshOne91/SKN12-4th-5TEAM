# Emergency Support Template Common Module

## 📌 개요
Emergency Support 템플릿의 공통 모듈입니다. 응급 의료 지원 관련 직렬화 스키마를 정의합니다.

## 🏗️ 구조
```
template/emergency_support/common/
└── emergency_support_serialize.py # 요청/응답 직렬화 스키마
```

## 📊 emergency_support_serialize.py

### 응급 지원 질의 스키마
```python
class EmergencySupportAskRequest(BaseRequest):
    question: str  # 응급 상황 관련 질문

class EmergencySupportAskResponse(BaseResponse):
    answer: str    # RAG 시스템이 생성한 응답
```

## 💡 설계 특징

1. **단순한 구조**: 질문과 응답만 정의
2. **함수 기반 RAG 연동**: `get_rag_answer_async()` 함수 지원
3. **BaseRequest/BaseResponse 상속**: 공통 프로토콜 준수  
4. **응급 상황 특화**: 생명과 직결된 응급 의료 질의 처리

이 모듈은 **응급 의료 지원 RAG 시스템의 계약**을 정의하는 **생명 구조 스키마 계층**입니다.