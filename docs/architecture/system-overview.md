# 시스템 개요

## 1. 시스템 목적

FabGraph는 반도체 제조 데이터를 대상으로, 자연어 질의를 SQL / Cypher / 분석 도구 실행으로 변환하고 그 결과를 하나의 워크스페이스에서 통합 제공하는 시스템입니다.

현재 구현은 thin-slice 중심이지만, 최종적으로는 **실데이터 기반 질의 + 구조화된 에이전트 오케스트레이션**을 지원하는 방향을 목표로 합니다.

---

## 2. 상위 구조

```text
사용자
  -> 프론트엔드 워크스페이스
  -> Chat API
  -> Router Agent
     -> SQL Agent -> PostgreSQL
     -> Cypher Agent -> Neo4j
     -> Viz Agent
     -> Synthesis Agent
  -> 구조화된 결과(Artifacts)
     -> Table
     -> Graph
     -> Chart
     -> Text Answer
```

---

## 3. 핵심 원칙

- PostgreSQL은 정형 조회와 집계의 주 DB로 사용한다.
- Neo4j는 관계 탐색, 계보 추적, 그룹 탐색의 주 DB로 사용한다.
- LLM은 오케스트레이션과 해석을 담당한다.
- 계산은 Python 기반 도구가 담당한다.
- 프론트엔드는 구조화된 결과 artifact를 렌더링하는 방향으로 설계한다.

---

## 4. 질의 처리 흐름

1. 사용자가 자연어 질문을 입력한다.
2. Router Agent가 의도와 실행 계획을 만든다.
3. SQL Agent 또는 Cypher Agent, 필요하면 둘 다 실행한다.
4. Viz Agent가 차트 스펙을 생성한다.
5. Synthesis Agent가 최종 텍스트 답변을 만든다.
6. 프론트엔드는 그래프, 테이블, 차트, 설명을 함께 보여준다.

---

## 5. 프론트엔드 구성

- Workspace shell
- Query panel
- Chat panel
- Graph view
- Table view
- Chart view
- Detail panel

선택 상태는 중앙 store에서 공유한다.

---

## 6. 백엔드 구성

- API routes
- DB access layer
- Agent orchestration layer
- Tool layer
- Metadata layer
- Response schema layer

---

## 7. 확장 포인트

- Analytics Agent 추가
- 예측 모델 도구 추가
- 메타데이터 자동 갱신 파이프라인 추가
- 인증 / 권한 시스템 추가
