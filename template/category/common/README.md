# Category Template Common Module

## 📌 개요
Category 템플릿의 공통 모듈입니다. 의료 질문 분류 관련 직렬화 스키마를 정의합니다.

## 🏗️ 구조
```
template/category/common/
└── category_serialize.py # 요청/응답 직렬화 스키마
```

## 📊 category_serialize.py

### 분류 질의 스키마
```python
class CategoryAskRequest(BaseRequest):
    question: str  # 분류할 의료 질문

class CategoryAskResponse(BaseResponse):
    answer: str    # 분류된 서비스의 응답
```

## 💡 설계 특징

1. **단순한 구조**: 질문과 응답만 정의
2. **BaseRequest/BaseResponse 상속**: 공통 프로토콜 준수
3. **문자열 기반**: 자연어 질문과 응답 처리

이 모듈은 **의료 질문 분류 시스템의 계약**을 정의하는 **데이터 스키마 계층**입니다.