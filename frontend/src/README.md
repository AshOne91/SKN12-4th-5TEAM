# Frontend Source Code

## 📌 개요
React 애플리케이션의 **소스 코드**를 포함하는 폴더입니다. 의료 챗봇 서비스의 프론트엔드 컴포넌트, 스타일, 설정 파일들을 포함합니다.

## 🏗️ 구조
```
frontend/src/
├── App.js              # 메인 앱 컴포넌트 및 라우팅
├── App.css             # 앱 전역 스타일
├── App.test.js         # 앱 테스트 파일
├── Landing.js          # 랜딩 페이지 컴포넌트
├── Landing.css         # 랜딩 페이지 스타일
├── Login.js            # 로그인 페이지 컴포넌트
├── Login.css           # 로그인 페이지 스타일
├── Signup.js           # 회원가입 페이지 컴포넌트
├── ChatbotPage.js      # 챗봇 페이지 컴포넌트
├── ChatbotPage.css     # 챗봇 페이지 스타일
├── Welcome.js          # 환영 페이지 컴포넌트
├── config.js           # 설정 파일
├── index.js            # React 엔트리포인트
├── index.css           # 글로벌 CSS
├── logo.svg            # React 로고
├── reportWebVitals.js  # 성능 측정
├── setupTests.js       # 테스트 설정
└── public/
    └── background.mp4  # 배경 동영상 (중복)
```

## 🛣️ 라우팅 구조 (App.js)

### 실제 라우트 설정
```javascript
<Router>
  <Routes>
    <Route path="/" element={<Landing />} />
    <Route path="/login" element={<Login />} />
    <Route path="/signup" element={<Signup />} />
    <Route path="/chatbot" element={<ChatbotPage />} />
  </Routes>
</Router>
```

**페이지 구성**:
- `/` - 랜딩 페이지 (서비스 소개)
- `/login` - 로그인
- `/signup` - 회원가입  
- `/chatbot` - 의료 챗봇 인터페이스

## 📱 주요 컴포넌트

### Landing.js
- 서비스 메인 페이지
- 배경 동영상 활용
- 로그인/회원가입으로 라우팅

### Login.js / Signup.js
- 사용자 인증 인터페이스
- 백엔드 API 연동 (chatbot_server)

### ChatbotPage.js
- 의료 챗봇 대화 인터페이스
- 실시간 채팅 UI
- 채팅방 관리

### Welcome.js
- 환영 페이지 (사용 여부 불명)

## ⚙️ 설정 및 구성

### config.js
```javascript
// 백엔드 API 엔드포인트 설정
```

### index.js
```javascript
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
// React 18+ 방식으로 앱 마운팅
```

## 🎨 스타일링

- **CSS Modules 미사용**: 각 컴포넌트별 개별 CSS 파일
- **글로벌 스타일**: index.css, App.css
- **컴포넌트별 스타일**: Landing.css, Login.css, ChatbotPage.css

## 📦 사용된 라이브러리 (package.json 기반)

### 핵심 라이브러리
- `react: ^19.1.0` - React 메인 라이브러리
- `react-dom: ^19.1.0` - DOM 렌더링
- `react-router-dom: ^7.6.2` - 클라이언트 사이드 라우팅

### UI/UX
- `react-icons: ^5.5.0` - 아이콘 컴포넌트
- `react-transition-group: ^4.4.5` - 애니메이션 전환

### 테스팅
- `@testing-library/react: ^16.3.0` - React 컴포넌트 테스팅
- `@testing-library/jest-dom: ^6.6.3` - DOM 테스팅 유틸리티

### 빌드/개발
- `react-scripts: 5.0.1` - Create React App 빌드 도구

## 💡 실제 코드 특징

1. **Create React App 기반**: 표준 CRA 구조 사용
2. **함수형 컴포넌트**: 최신 React Hooks 패턴
3. **SPA 구조**: react-router-dom으로 클라이언트 라우팅
4. **의료 서비스 UI**: 챗봇 중심의 의료 상담 인터페이스
5. **반응형 디자인**: CSS를 통한 모바일 대응

이 폴더는 **의료 챗봇 서비스의 사용자 인터페이스**를 구현하는 **React 프론트엔드 애플리케이션**입니다.