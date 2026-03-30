# FabGraph 백엔드 스켈레톤

FabGraph 백엔드는 FastAPI 기반으로 구성되어 있으며, 현재는 아래 기능을 중심으로 뼈대를 갖추고 있습니다.

- 채팅 API
- SQL 질의 API
- Cypher 질의 API
- 스키마 조회 API
- 헬스체크 API

현재 일부 엔드포인트는 thin-slice / placeholder 성격을 포함하고 있으며, 이후 실제 PostgreSQL / Neo4j / agent orchestration 로직으로 점진적으로 교체될 예정입니다.
