# FabGraph 프론트엔드 스켈레톤

이 프론트엔드는 Vite 기반 React 앱으로 구성되어 있으며, `cypher-graph`에서 재사용 가치가 높은 화면과 상태 구조를 선별 이식해 시작했습니다.

## 현재 포함된 것
- App shell
- 채팅 패널
- 그래프 뷰
- 테이블 뷰
- 쿼리 / 차트 / 상세 패널 기본 구조
- Zustand store
- API client / schema 기초 구조

## 현재 남아 있는 갭
- shadcn/ui 기반 컴포넌트는 최소 local stub로 대체된 부분이 있음
- 스타일링은 아직 임시 성격이 강함
- conversation history는 stub 상태
- backend contract는 FabGraph 방향에 맞춰 계속 정렬해야 함

즉, 현재 프론트는 **데모 가능한 작업용 스켈레톤**으로 보는 것이 맞고, 이후 도메인 UX에 맞춰 계속 다듬어야 합니다.
