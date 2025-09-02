# Internal External Template Common Module

## 📌 개요
Internal External 템플릿의 공통 모듈입니다. 내과/외과 구분 관련 직렬화 스키마를 정의합니다.

## 🏗️ 구조
```
template/internal_external/common/
└── internal_external_serialize.py # 요청/응답 직렬화 스키마
```

## 📊 internal_external_serialize.py

### 내과/외과 구분 질의 스키마
```python
class InternalExternalAskRequest(BaseRequest):
    question: str  # 내과/외과 관련 질문

class InternalExternalAskResponse(BaseResponse):
    answer: str    # RAG 시스템이 생성한 응답
```

## 💡 설계 특징

1. **단순한 구조**: 질문과 응답만 정의
2. **함수 기반 RAG 연동**: Emergency Support와 동일한 RAG 함수 사용
3. **BaseRequest/BaseResponse 상속**: 공통 프로토콜 준수
4. **진료과 특화**: 내과/외과 구분 및 치료 방향 제시

이 모듈은 **내과/외과 구분 RAG 시스템의 계약**을 정의하는 **진료과 라우팅 스키마 계층**입니다.