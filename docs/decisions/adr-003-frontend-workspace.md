# ADR-003: Workspace UI 유지

## 상태
제안

## 결정
기존 `cypher-graph`의 Graph / Table / Chart / Chat 중심 워크스페이스 UI 패턴을 유지한다.

## 이유
- 이미 탐색형 제품에 적합한 UX가 검증돼 있다.
- 재사용 가치가 높다.
- backend가 바뀌어도 frontend shell은 유지할 수 있다.

## 결과
- QueryPanel과 ChartView는 개편이 필요하다.
- artifact 중심 렌더링 계약이 중요해진다.
