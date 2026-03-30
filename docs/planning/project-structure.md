# 프로젝트 구조 초안

## 권장 루트 구조

```text
fabgraph/
├─ README.md
├─ docs/
│  ├─ product/
│  ├─ architecture/
│  ├─ decisions/
│  └─ planning/
├─ infra/
│  ├─ docker-compose.yml
│  ├─ postgres/
│  └─ neo4j/
├─ backend/
│  ├─ pyproject.toml
│  ├─ app/
│  │  ├─ main.py
│  │  ├─ core/
│  │  ├─ api/
│  │  │  └─ routes/
│  │  ├─ db/
│  │  │  ├─ postgres/
│  │  │  └─ neo4j/
│  │  ├─ agents/
│  │  ├─ tools/
│  │  ├─ metadata/
│  │  ├─ schemas/
│  │  └─ services/
│  └─ tests/
├─ frontend/
│  ├─ package.json
│  └─ src/
│     ├─ app/
│     ├─ pages/
│     ├─ features/
│     ├─ entities/
│     ├─ shared/
│     └─ store/
└─ samples/
   └─ seed-data/
```

## backend 세부 구조

```text
backend/app/
├─ main.py
├─ core/
│  ├─ config.py
│  ├─ logging.py
│  └─ exceptions.py
├─ api/routes/
│  ├─ chat.py
│  ├─ query_sql.py
│  ├─ query_cypher.py
│  ├─ schema.py
│  └─ health.py
├─ db/postgres/
│  ├─ engine.py
│  ├─ models.py
│  ├─ repositories/
│  └─ migrations/
├─ db/neo4j/
│  ├─ client.py
│  ├─ schema.py
│  └─ repositories/
├─ agents/
│  ├─ router/
│  ├─ sql/
│  ├─ cypher/
│  ├─ viz/
│  └─ synthesis/
├─ tools/
│  ├─ sql_tools/
│  ├─ graph_tools/
│  ├─ analytics_tools/
│  └─ viz_tools/
├─ metadata/
│  ├─ domain_dictionary/
│  ├─ prompt_examples/
│  └─ schema_cache/
└─ schemas/
```

## frontend 세부 구조

```text
frontend/src/
├─ app/
├─ pages/workspace/
├─ features/
│  ├─ chat/
│  ├─ graph/
│  ├─ table/
│  ├─ chart/
│  ├─ query/
│  └─ detail/
├─ entities/
│  ├─ graph/
│  ├─ query/
│  └─ artifact/
├─ shared/
│  ├─ api/
│  ├─ ui/
│  └─ utils/
└─ store/
```

## FabGraph 초기 이식 우선순위

1. `App.tsx`
2. `ChatPanel.tsx`
3. `GraphView.tsx`
4. `TableView.tsx`
5. store / api client
6. QueryPanel / ChartView는 재설계 후 이식
