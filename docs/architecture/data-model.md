# 데이터 모델

## 1. 설계 원칙

- PostgreSQL = 단일 진실 공급원(Single Source of Truth)
- Neo4j = 관계 탐색 / 그래프 탐색 레이어
- 공통 키는 `wafer_id`

---

## 2. PostgreSQL 핵심 테이블

### wafer
- wafer_id
- lot_id
- product_code
- created_at

### process_history
- id
- wafer_id
- stepseq
- ppid
- eqp
- chamber
- rf_time
- tkin_time
- tkout_time
- step_order

### target_process
- id
- wafer_id
- stepseq
- ppid
- eqp
- chamber
- rf_time
- tkin_time
- tkout_time
- main_steps(JSONB)

### recipe_param
- id
- target_process_id
- step_name
- param_name
- param_value

### metrology_2d
- id
- wafer_id
- metric_name
- shot_position
- value

### metrology_3d
- id
- wafer_id
- metric_name
- shot_position
- wl_position
- value

---

## 3. Neo4j 핵심 모델

### 노드(Node)
- Wafer
- Lot
- DOE
- Equipment
- Chamber
- Recipe
- ProcessStep
- Metrology

### 관계(Relationship)
- BELONGS_TO
- CONTAINS
- PROCESSED
- HAS
- APPLIED_TO
- EVOLVED_TO
- AT_STEP
- NEXT
- MEASURED

---

## 4. 설계 포인트

- 레시피는 EAV 패턴으로 풀어서 SQL 필터링이 가능하게 저장한다.
- 원본 레시피 구조는 JSONB로 보존한다.
- 계측은 위치별 행 분리 방식으로 저장해 집계 가능성을 높인다.
- Neo4j에는 상세 수치보다는 관계 중심 데이터만 저장한다.

---

## 5. 후속 검토 항목

- DOE를 PostgreSQL에도 보조 테이블로 둘지 여부
- step dictionary / equipment dictionary 관리 방식
- 2D wafer map 좌표계 표준화 방식
