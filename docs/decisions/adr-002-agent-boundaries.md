# ADR-002: Agent 책임 분리

## 상태
제안

## 결정
Coordinator 단일 구조 대신 Router / SQL / Cypher / Viz / Synthesis로 책임을 분리한다.

## 이유
- 질의 계획과 실제 실행 책임을 분리할 수 있다.
- 디버깅과 확장이 쉬워진다.
- Analytics Agent를 나중에 독립적으로 추가하기 쉽다.

## 결과
- 응답 계약을 더 구조화해야 한다.
- agent context 관리가 중요해진다.
