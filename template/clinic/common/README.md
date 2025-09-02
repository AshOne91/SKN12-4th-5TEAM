# Clinic Template Common Module

## 📌 개요
Clinic 템플릿의 공통 모듈입니다. 병원 및 의료진 정보 관련 직렬화 스키마를 정의합니다.

## 🏗️ 구조
```
template/clinic/common/
└── clinic_serialize.py # 요청/응답 직렬화 스키마
```

## 📊 clinic_serialize.py

### 병원 정보 질의 스키마
```python
class ClinicAskRequest(BaseRequest):
    question: str  # 병원/의료진 관련 질문

class ClinicAskResponse(BaseResponse):
    answer: str    # RAG 시스템이 생성한 응답
```

## 💡 설계 특징

1. **단순한 구조**: 질문과 응답만 정의
2. **RAG 시스템 연동**: FAISS + GPT-4o 응답 처리
3. **BaseRequest/BaseResponse 상속**: 공통 프로토콜 준수
4. **자연어 기반**: 병원 정보에 대한 자연어 질의 지원

이 모듈은 **병원 정보 RAG 시스템의 계약**을 정의하는 **데이터 스키마 계층**입니다.