# 현재 구현과 설계 문서의 차이

이 문서는 FabGraph의 **현재 코드 상태**와 **장기 설계 문서** 사이의 차이를 빠르게 파악하기 위한 메모입니다.

## 현재 구현된 것

- backend / frontend 실행 가능
- PostgreSQL / Neo4j 로컬 개발 훅 존재
- DB가 없어도 sample fallback으로 동작 가능
- UC1 최신 웨이퍼 조회 동작
- UC2 조건 필터 + 기본 통계 동작
- UC3 동일 기간 / DOE 스타일 그룹 탐색 동작
- backend 테스트 일부 존재
- frontend build 가능

## 아직 설계 수준에 머물러 있는 것

- Router / SQL / Cypher / Synthesis Agent의 본격 분리 구현
- 범용 SQL query planner
- 범용 Cypher query engine
- 실제 Neo4j 기반 심화 DOE 탐색
- 실데이터 스키마 반영
- 인증 / 대화 저장 / 운영 기능
- Analytics Agent / Viz Agent의 본격 고도화

## 현재 코드 관점에서 보면

FabGraph는 지금 **구조를 검증하는 thin-slice 제품**에 가깝습니다.
즉,
- UX 흐름은 확인 가능하고
- API 계약도 어느 정도 잡혀 있지만
- 내부 오케스트레이션과 실제 데이터 모델은 앞으로 더 자라야 합니다.

## 문서를 읽을 때 권장 기준

- 제품 방향 확인: `docs/product/prd.md`
- 시스템 큰 그림 확인: `docs/architecture/system-overview.md`
- 현재 실행 방법 확인: `README.md`
- 지금 상태와 다음 할 일 확인: 워크스페이스의 `STATUS.md`, `NEXT_STEPS.md`
