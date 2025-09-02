# Frontend Source Public Assets

## 📌 개요
Frontend 소스 코드 내의 **공개 자산 폴더**입니다. 소스 코드에서 직접 참조하는 미디어 파일을 포함합니다.

## 🏗️ 구조
```
frontend/src/public/
└── background.mp4    # 배경 동영상 파일
```

## 🎬 background.mp4

### 실제 사용
- **위치**: `/frontend/src/public/background.mp4`
- **중복**: `/frontend/public/background.mp4`와 동일한 파일
- **용도**: React 컴포넌트에서 배경 동영상으로 활용

### 예상 사용 패턴
```javascript
// src 폴더 내에서 import 방식
import backgroundVideo from './public/background.mp4';

// 또는 public 경로 직접 참조
<video src="/background.mp4" />
```

## 💡 구조적 특징

1. **중복 파일**: `/frontend/public/background.mp4`와 동일
2. **소스 내 위치**: src 폴더 내부에 위치
3. **직접 참조**: 컴포넌트에서 상대 경로로 접근 가능

**주의**: 일반적으로 정적 자산은 `/public` 폴더에만 위치하는 것이 표준이므로, 이 위치의 파일은 중복이거나 개발 과정에서 생긴 잔여 파일일 가능성이 있습니다.

이 폴더는 **소스 코드 레벨에서의 미디어 자산 관리**를 위한 공간이지만, 표준 React 프로젝트 구조와는 다른 패턴입니다.