# 스프린트 분해안

## Sprint 0 — 방향 확정

### 목표
구현 전에 제품 범위와 구조를 고정한다.

### 작업
- 프로젝트명 확정
- MVP 범위(UC1~UC3) 확정
- PRD / ADR / API 문서 검토
- 기존 `cypher-graph`에서 재사용 범위 확정

### 완료 기준
- 설계 문서 리뷰 완료
- 새 repo 생성 여부 결정 완료

---

## Sprint 1 — Skeleton + Data Foundation

### 목표
실행 가능한 기본 골격과 데이터 연결 준비

### backend
- FastAPI skeleton 생성
- config/settings 체계 생성
- PostgreSQL engine/session 생성
- Neo4j client 생성
- health endpoint 생성
- schema endpoints 생성

### data
- PostgreSQL 스키마 초안 작성
- 샘플 seed 데이터 작성
- Neo4j seed / sync 방식 정의

### frontend
- Vite app skeleton 생성
- workspace shell 이식
- 기본 store 구성

### 완료 기준
- 백엔드 / 프론트 구동 확인
- 두 DB 연결 확인

---

## Sprint 2 — Query Layer

### 목표
직접 질의 경로를 완성한다.

### 작업
- `/api/query/sql` 구현
- `/api/query/cypher` 구현
- query validation 추가
- graph/table artifact 변환기 구현
- frontend에서 SQL / Cypher 결과 렌더링 연결

### 완료 기준
- 구조화된 query 결과를 프론트에서 확인 가능

---

## Sprint 3 — Agent Orchestration MVP

### 목표
자연어 -> Router -> SQL / Cypher -> 응답 흐름 연결

### 작업
- Router Agent 초안
- SQL Agent 초안
- Cypher Agent 초안
- Synthesis Agent 초안
- streaming chat route 구현
- steps 표시 연결

### 완료 기준
- 자연어로 UC1 / UC2 / UC3 데모 가능

---

## Sprint 4 — Visualization & UX polish

### 목표
artifact 기반 시각화 완성도 향상

### 작업
- ChartView 개편
- QueryPanel 개편
- Detail panel 고도화
- 그래프 / 테이블 / 차트 상호작용 개선
- empty / error / loading 상태 정리

### 완료 기준
- 내부 데모 가능한 UX 확보

---

## Sprint 5 — Analytics Phase 2 Entry

### 목표
분석 기능 기반 추가

### 작업
- 통계 도구 추가
- 이상치 탐지 추가
- 상관분석 추가
- Viz Agent 개선

### 완료 기준
- 분석형 질문에 대해 구조화된 리포트 제공 가능
