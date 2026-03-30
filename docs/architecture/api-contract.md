# API 계약 초안

## 1. 목적

프론트엔드가 agent 내부 구현에 과하게 종속되지 않도록, 결과 계약을 명확한 artifact 중심으로 정의합니다.

---

## 2. 주요 엔드포인트

### POST /api/chat/stream
입력 예시:
```json
{
  "message": "UR123111 최신 wafer 20개 보여줘",
  "history": [],
  "context": {
    "selected_node": null,
    "selected_row": null
  }
}
```

출력 이벤트:
- `plan`
- `step_start`
- `step_end`
- `token`
- `done`
- `error`

### POST /api/query/sql
- 구조화된 SQL 실행 결과 반환

### POST /api/query/cypher
- 구조화된 Cypher 실행 결과 반환

### GET /api/schema/postgres
- PostgreSQL schema 정보 반환

### GET /api/schema/graph
- Graph schema 정보 반환

---

## 3. done payload 초안

```json
{
  "message": "최근 웨이퍼 20개를 조회했습니다.",
  "plan": {
    "intent": "latest_wafers_lookup",
    "agents": ["sql_agent", "viz_agent", "synthesis_agent"]
  },
  "artifacts": {
    "table": [],
    "graph": {
      "nodes": [],
      "edges": [],
      "raw": []
    },
    "charts": []
  },
  "steps": [],
  "errors": []
}
```

---

## 4. 프론트 렌더링 원칙

- 테이블은 `artifacts.table`
- 그래프는 `artifacts.graph`
- 차트는 `artifacts.charts`
- 요약 설명은 `message`
- 중간 과정은 `steps`

---

## 5. 확장 방향

향후 `analytics_results`, `recommendations`, `confidence`, `citations` 같은 필드를 추가할 수 있게 여지를 둡니다.
