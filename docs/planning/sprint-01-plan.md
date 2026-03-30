# Sprint 01 계획

## 목적
새 프로젝트의 설계 기반과 구현 골격을 동시에 만드는 것.

## 작업 목록

### 문서
- [ ] 프로젝트명 확정
- [ ] PRD 검토 / 보완
- [ ] ADR 3개 확정
- [ ] API contract 검토

### backend
- [ ] FastAPI skeleton 생성
- [ ] PostgreSQL 연결 레이어 추가
- [ ] Neo4j client 레이어 분리
- [ ] `/api/query/sql` 추가
- [ ] `/api/query/cypher` 추가
- [ ] `/api/schema/postgres` 추가
- [ ] `/api/schema/graph` 추가
- [ ] Router Agent 초안 추가

### frontend
- [ ] App shell 이식
- [ ] ChatPanel 이식
- [ ] GraphView 이식
- [ ] TableView 이식
- [ ] QueryPanel 재설계
- [ ] ChartView 재설계
- [ ] artifact 기반 렌더링 계약 반영

### data
- [ ] sample data format 정의
- [ ] postgres seed script 작성
- [ ] neo4j seed 또는 sync script 작성

## 산출물
- 실행 가능한 skeleton repo
- 설계 문서 세트
- 첫 데모용 sample data 흐름
