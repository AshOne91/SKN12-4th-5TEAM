# Drug Template Common Module

## 📌 개요
Drug 템플릿의 공통 모듈입니다. 약품 정보 관련 직렬화 스키마를 정의합니다.

## 🏗️ 구조
```
template/drug/common/
└── drug_serialize.py # 요청/응답 직렬화 스키마
```

## 📊 drug_serialize.py

### 약품 정보 질의 스키마
```python
class DrugAskRequest(BaseRequest):
    question: str  # 약품 관련 질문

class DrugAskResponse(BaseResponse):
    answer: str    # RAG 시스템이 생성한 응답
```

## 💡 설계 특징

1. **단순한 구조**: 질문과 응답만 정의
2. **Vector_store 연동**: 클래스 기반 RAG 시스템 지원
3. **BaseRequest/BaseResponse 상속**: 공통 프로토콜 준수
4. **약품 전문화**: 의약품 관련 자연어 질의 특화

이 모듈은 **약품 정보 RAG 시스템의 계약**을 정의하는 **데이터 스키마 계층**입니다.