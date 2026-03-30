# FabGraph

FabGraph는 **반도체 제조 데이터를 자연어로 탐색하고, 그래프·테이블·차트로 함께 확인할 수 있는 분석 워크스페이스**입니다.

이 프로젝트는 기존 `cypher-graph`의 후속 프로젝트로 시작했으며, 현재는 **작지만 끝까지 이어지는 thin-slice 제품 형태**를 목표로 개발 중입니다.  
지금 단계에서는 아래 3개 유스케이스를 중심으로 동작합니다.

- **UC1**: 최신 웨이퍼 조회
- **UC2**: 조건 필터링 + 기본 통계
- **UC3**: 동일 기간 / DOE 스타일 그룹 탐색

DB가 없어도 바로 데모할 수 있도록 **샘플 데이터 fallback**을 제공하며, 필요하면 PostgreSQL + Neo4j 로컬 환경으로 확장해서 개발할 수 있습니다.

---

## FabGraph가 지향하는 방향

FabGraph는 단순히 그래프를 예쁘게 보여주는 앱이 아니라, 다음을 지향합니다.

- 자연어 기반 반도체 제조 데이터 탐색
- PostgreSQL + Neo4j 하이브리드 구조
- 그래프 / 테이블 / 차트 / 채팅이 연결된 단일 워크스페이스
- 앞으로 Router / SQL / Cypher / Synthesis Agent 구조로 확장 가능한 기반

현재 구현은 초기 thin slice 수준이지만, 이후 실데이터와 실제 질의 흐름으로 고도화하기 좋은 형태를 목표로 하고 있습니다.

---

## 현재 구현 상태

### 지금 가능한 것
- PostgreSQL / Neo4j 로컬 연결 훅 제공
- DB가 꺼져 있어도 샘플 웨이퍼 데이터로 fallback 동작
- **UC1 최신 웨이퍼 조회** 동작
- **UC2 조건 필터링 + 기본 통계** 동작
- **UC3 동일 기간 / DOE 스타일 그룹 탐색** 동작
- 프론트엔드에서 그래프 / 테이블 / 차트 렌더링 가능

### 아직 한계가 있는 부분
- `/api/query/cypher`는 아직 범용 Cypher 엔진이 아니라 thin-slice adapter에 가깝습니다.
- UC2 필터링은 현재 `status / recipe_id / lot_id` 중심으로만 지원합니다.
- UC3는 아직 실제 Neo4j 기반 심화 탐색보다 fallback 비중이 큽니다.
- QueryPanel은 아직 진짜 query planner라기보다 preset 중심 command surface에 가깝습니다.

---

## 빠른 실행 방법

## 1) Backend 실행

```bash
cd backend
uv sync --extra dev
cp ../.env.example ../.env  # 선택 사항
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 2) Frontend 실행

```bash
cd frontend
npm install
npm run dev
```

접속 주소:
- Frontend: http://localhost:5174
- Backend docs: http://localhost:8000/docs

---

## DB 없이 가장 빠르게 데모하는 방법

아래처럼 backend와 frontend만 켜도 됩니다.

```bash
cd /home/bjpark/projects/fabgraph/backend
uv sync --extra dev
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

cd /home/bjpark/projects/fabgraph/frontend
npm install
npm run dev
```

이 경우 PostgreSQL이 없어도 **샘플 JSON fallback**으로 UC1~UC3를 바로 확인할 수 있습니다.

---

## 로컬 DB까지 포함해서 실행하기

### 1) PostgreSQL + Neo4j 실행

```bash
cd infra
docker compose up -d
```

PostgreSQL은 `infra/postgres/init/` 안의 schema + seed SQL을 사용합니다.

### 2) PostgreSQL 재시드(선택)

```bash
cd backend
uv run --env-file ../.env python ../scripts/seed_postgres.py
```

### 3) Neo4j 샘플 데이터 import(선택)

```bash
docker exec -i fabgraph-neo4j cypher-shell -u neo4j -p fabgraph123 < /seed/seed.cypher
```

---

# 유스케이스별 안내

## UC1 — 최신 웨이퍼 조회

### 현재 되는 것
- `/api/chat`, `/api/chat/stream`에서 최신 웨이퍼 질문 처리
- `/api/query/cypher`를 통해 최신 웨이퍼 graph view 생성
- PostgreSQL이 없어도 sample fallback으로 동작

### 예시 질문
- `최근 wafer 10개 알려줘`
- `latest wafers 보여줘`

### 프론트 preset
- `UC1 최신 Wafer`

---

## UC2 — 조건 필터링 + 기본 통계

### 현재 되는 것
- 채팅에서 `hold`, `queued`, `processed`, `R-*`, `L-*` 같은 조건 감지
- `/api/query/sql`에서 필터링 + 통계 응답 반환
- `/api/query/cypher`에서 그래프/테이블 렌더용 결과 반환
- 채팅 응답에 기본 통계와 차트 설정 포함

### 예시 질문
- `hold 상태 wafer만 필터해서 통계 보여줘`
- `processed wafer 통계 보여줘`
- `L-2002 lot wafer 필터 결과 보여줘`

### 예시 명령

```bash
curl -s http://localhost:8000/api/chat \
  -H 'Content-Type: application/json' \
  -d '{"message":"hold 상태 wafer만 필터해서 통계 보여줘"}'

curl -s http://localhost:8000/api/query/sql \
  -H 'Content-Type: application/json' \
  -d '{"query":"-- uc2 filtered wafers","parameters":{"mode":"uc2","status":"hold"}}'
```

### 프론트 preset
- `UC2 조건 + 통계`

---

## UC3 — 동일 기간 / DOE 스타일 그룹 탐색

### 현재 되는 것
- 채팅에서 same-period / DOE / group exploration 의도 감지
- `/api/query/cypher`에서 탐색 루트 + 그룹 노드 + recipe link 반환
- Neo4j 사용 가능 여부를 source 힌트로 반영
- Neo4j가 없어도 deterministic fallback으로 동작
- 프론트 그래프/테이블/차트에서 결과 렌더 가능

### 예시 질문
- `동일 기간 lot 그룹 탐색 보여줘`
- `same period DOE group exploration`
- `recipe 기준 그룹 탐색 보여줘`

### 예시 명령

```bash
curl -s http://localhost:8000/api/query/cypher \
  -H 'Content-Type: application/json' \
  -d '{"query":"// uc3 same period DOE exploration","parameters":{"mode":"uc3","group_by":"lot_id"}}'
```

### 프론트 preset
- `UC3 동일기간 그룹`

---

## 검증 방법

### Backend 테스트

```bash
cd /home/bjpark/projects/fabgraph/backend
uv sync --extra dev
uv run pytest
```

### Frontend 빌드

```bash
cd /home/bjpark/projects/fabgraph/frontend
npm install
npm run build
```

---

## 다음 단계

다음 단계에서는 아래를 우선 목표로 확장합니다.
- 실제 데이터 샘플 반영
- PostgreSQL 실쿼리 강화
- Neo4j 기반 DOE / group 탐색 고도화
- Router / SQL / Cypher / Synthesis agent 구조 실제화
- 이후 UC4~UC6 방향 확장
