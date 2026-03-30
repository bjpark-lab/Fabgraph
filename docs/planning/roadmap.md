# 로드맵

## 현재 위치

현재 FabGraph는 **UC1~UC3 중심 thin-slice MVP** 단계에 있습니다.  
즉, 작은 범위지만 실제 화면과 API 흐름이 끝까지 이어지는 형태를 우선 확보한 상태입니다.

---

## Phase 1 — 탐색 MVP
- UC1 최신 웨이퍼 조회
- UC2 조건 필터링 + 기본 통계
- UC3 DOE / 동시기 그룹 탐색
- Graph / Table / Chart / Chat 워크스페이스
- SQL / Cypher 이중 질의 경로

## Phase 2 — 분석 강화
- 이상치 탐지
- 상관 분석
- 차트 추천
- 분석 리포트 강화
- Analytics Agent 추가

## Phase 3 — 예측 / 추천
- 레시피 -> 계측 예측
- 계측 -> 레시피 탐색
- feature importance
- 신뢰도 / 설명 가능성 리포트

---

## FabGraph Phase 1 가드레일
- 범위는 UC1~UC3로 고정
- `cypher-graph`의 UX 패턴은 재사용하되, 기존 결합 구조는 그대로 끌고 가지 않음
- 이후 agent orchestration을 위해 SQL / Cypher 실행 경로를 명시적으로 유지
- 실데이터 반영 전까지는 fallback/sample path를 적극 활용
