# Internal External Vector Database (uiheon)

## 📌 개요
Internal External 서비스를 위한 **내과/외과 구분 벡터 데이터베이스**입니다. FAISS 인덱스와 텍스트 청크를 포함하여 내과/외과 질의응답을 지원합니다.

## 🏗️ 구조
```
resources/vectorDB/uiheon/
├── QA_random_pair_part1_chunks1.txt  # 내과/외과 텍스트 청크
└── QA_random_pair_part1_index1.index # FAISS 벡터 인덱스
```

## 📄 데이터 구성

### QA_random_pair_part1_chunks1.txt
- **내용**: 내과/외과 구분에 대한 질문-답변 쌍의 텍스트 청크
- **형식**: 텍스트 파일 (UTF-8 인코딩)
- **용도**: RAG 시스템에서 컨텍스트로 활용

### QA_random_pair_part1_index1.index
- **내용**: FAISS 벡터 인덱스 파일
- **형식**: FAISS 바이너리 인덱스
- **용도**: 질문 임베딩과 유사도 검색

## ⚖️ 내과/외과 도메인

이 벡터 DB가 다루는 내과/외과 구분 정보:
- **내과 질환**: 내부 장기 질병, 만성질환, 내과적 치료
- **외과 질환**: 수술적 치료 대상, 외상, 종양
- **구분 기준**: 증상에 따른 적절한 진료과 추천
- **치료 방향**: 보존적 치료 vs 수술적 치료 판단

## 🔗 연동 방식

### Internal External Template에서 사용
```python
# 환경변수로 경로 설정
INDEX_PATH = os.getenv("INTERNAL_EXTERNAL_VECTORDB_INDEX")
CHUNK_PATH = os.getenv("INTERNAL_EXTERNAL_VECTORDB_TXT")

# 초기화 시 로드
self.index = load_faiss_index(INDEX_PATH)
self.chunks = load_chunks(CHUNK_PATH)
```

### 검색 플로우
1. 증상/질병 질문을 임베딩으로 변환
2. FAISS 인덱스에서 유사 벡터 검색
3. 해당하는 텍스트 청크 조회
4. 내과/외과 구분 정보로 LLM 응답 생성

## 💡 실제 파일 특징

- **폴더명**: `uiheon` (의헌) - 개발자명 또는 데이터 구분자
- **파일명**: `part1`으로 emergency_support의 `part2`와 구분
- **번호 체계**: `chunks1.txt`, `index1.index`로 순서 관리
- **QA 형식**: 내과/외과 관련 질문-답변 쌍 데이터

## 🔄 Emergency Support와의 관계

| 구분 | Internal External (uiheon) | Emergency Support |
|------|---------------------------|-------------------|
| **폴더** | `uiheon/` | `emergency_support_vectorDB/` |
| **파일** | `part1_chunks1.txt` | `part2_chunks1.txt` |
| **도메인** | 내과/외과 구분 | 응급 의료 처치 |
| **RAG 함수** | 동일한 함수 사용 | 동일한 함수 사용 |

이 벡터 DB는 **적절한 진료과 선택**을 위한 **의료 라우팅 지식 저장소**입니다.