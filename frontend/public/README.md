# Frontend Public Assets

## 📌 개요
React 앱의 **정적 자산(Static Assets)**을 저장하는 폴더입니다. 웹 애플리케이션의 공개 파일들과 메타데이터를 포함합니다.

## 🏗️ 구조
```
frontend/public/
├── background.mp4      # 배경 동영상
├── favicon.ico        # 웹사이트 파비콘
├── index.html         # HTML 템플릿 (엔트리포인트)
├── logo192.png        # 192x192 로고
├── logo512.png        # 512x512 로고
├── manifest.json      # PWA 매니페스트
└── robots.txt         # 검색 엔진 크롤러 지시사항
```

## 🎬 미디어 파일

### background.mp4
- **용도**: 애플리케이션 배경 동영상
- **형식**: MP4 비디오 파일
- **실제 사용**: Landing 페이지 등에서 배경 요소로 활용

## 🖼️ 아이콘 및 로고

### favicon.ico
- **용도**: 브라우저 탭, 북마크 아이콘
- **형식**: ICO 파일

### logo192.png / logo512.png
- **용도**: PWA 앱 아이콘 (다양한 해상도 지원)
- **형식**: PNG 이미지

## 📋 설정 파일

### manifest.json
- **용도**: Progressive Web App (PWA) 설정
- **내용**: 앱 메타데이터, 아이콘, 테마 색상 등

### robots.txt
- **용도**: 검색 엔진 크롤러 접근 제어
- **내용**: 크롤링 허용/거부 규칙

### index.html
- **용도**: React 앱의 HTML 엔트리포인트
- **내용**: `<div id="root"></div>` 마운트 포인트 포함

## 🔗 실제 연동

### React 컴포넌트에서 사용
```javascript
// public 폴더의 파일들은 절대 경로로 접근
<video src="/background.mp4" />
<img src="/logo192.png" />
```

### build 시 처리
- `npm run build` 시 public 폴더 내용이 build 폴더로 복사
- 상대 경로 그대로 유지되어 배포

이 폴더는 **웹 애플리케이션의 정적 리소스 저장소**로서 브라우저에서 직접 접근 가능한 공개 자산들을 관리합니다.