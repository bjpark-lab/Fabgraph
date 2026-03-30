# 에이전트 아키텍처

## 1. 목표

자연어 질문을 구조화된 실행 계획으로 바꾸고, 각 전문 agent가 적절한 DB와 도구를 호출하도록 설계합니다.

---

## 2. Agent 구성

### Router Agent
역할:
- 자연어 질문을 execution plan으로 변환

출력 예시:
```json
{
  "intent": "latest_wafers_lookup",
  "agents": ["sql_agent", "viz_agent", "synthesis_agent"],
  "execution_order": "serial",
  "params": {
    "stepseq": "UR123111",
    "limit": 20
  }
}
```

### SQL Agent
역할:
- PostgreSQL 질의 생성 / 실행
- 필터링, 정렬, 집계 담당

### Cypher Agent
역할:
- Neo4j 질의 생성 / 실행
- 관계 탐색, 그룹 탐색 담당

### Viz Agent
역할:
- 결과 데이터를 chart spec으로 변환

### Synthesis Agent
역할:
- 실행 결과를 최종 자연어 답변으로 정리

---

## 3. Phase 1 범위

Phase 1에서는 아래 agent를 우선 필수로 둡니다.
- Router Agent
- SQL Agent
- Cypher Agent
- Viz Agent(간단 버전)
- Synthesis Agent(간단 버전)

Analytics Agent는 Phase 2에서 추가합니다.

---

## 4. Agent Context

```python
class AgentContext:
    plan: dict
    sql_results: dict | None
    cypher_results: dict | None
    viz_results: dict | None
    final_answer: str | None
    errors: list
```

---

## 5. 설계 원칙

- LLM이 직접 계산하지 않는다.
- Agent 간 전달 데이터는 구조화한다.
- tool 호출 결과는 재사용 가능한 artifact로 남긴다.
- streaming UX는 유지하되, backend 내부 책임은 분리한다.
