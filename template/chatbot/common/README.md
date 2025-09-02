# Chatbot Template Common Module

## 📌 개요
Chatbot 템플릿의 공통 모듈입니다. 챗봇 서비스 관련 데이터 모델과 직렬화 스키마를 정의합니다.

## 🏗️ 구조
```
template/chatbot/common/
├── chatbot_model.py     # 챗봇 데이터 모델
└── chatbot_serialize.py # 요청/응답 직렬화 스키마
```

## 📊 chatbot_serialize.py

### 채팅방 관련 스키마
- 채팅방 목록 조회: `ChatbotRoomsRequest/Response`
- 새 채팅방 생성: `ChatbotRoomNewRequest/Response`

### 메시지 관련 스키마
- 메시지 전송: `ChatbotMessageRequest/Response`
- 대화 히스토리: `ChatbotHistoryRequest/Response`

### 데이터 모델
- `ChatbotRoomInfo`: 채팅방 정보 (id, title)
- `ChatbotMessageHistoryItem`: 메시지 히스토리 (role, content)

## 📝 chatbot_model.py

챗봇 서비스의 도메인 모델들을 정의합니다.

## 💡 설계 특징

1. **채팅방 중심**: 룸 기반 대화 관리
2. **히스토리 지원**: 대화 내역 추적
3. **역할 구분**: user/bot 메시지 구분
4. **BaseRequest/BaseResponse 상속**: 공통 프로토콜 준수

이 모듈은 **의료 챗봇 시스템의 계약**을 정의하는 **데이터 스키마 계층**입니다.