// TODO(fabgraph): branding/layout migrated from cypher-graph. Rework copy, theming, and tab composition.
import { useQuery } from '@tanstack/react-query'
import { Separator } from '@/shared/ui/separator'
import { Badge } from '@/shared/ui/badge'
import { QueryPanel } from '@/features/query/QueryPanel'
import { GraphView } from '@/features/graph/GraphView'
import { TableView } from '@/features/table/TableView'
import { ChartView } from '@/features/chart/ChartView'
import { DetailPanel } from '@/features/detail/DetailPanel'
import { ChatPanel } from '@/features/chat/ChatPanel'
import { useWorkspaceStore } from '@/store/useWorkspaceStore'
import { checkHealth } from '@/shared/api/client'

function HealthBadge() {
  const { data, isError } = useQuery({
    queryKey: ['health'],
    queryFn: checkHealth,
    refetchInterval: 30000,
    retry: false,
  })

  if (isError) return <Badge variant="destructive" className="text-xs">백엔드 오프라인</Badge>
  if (!data) return <Badge variant="secondary" className="text-xs">연결 중...</Badge>

  return (
    <div className="flex items-center gap-3 text-xs text-muted-foreground">
      <div className="flex items-center gap-1.5">
        <span className={`w-2 h-2 rounded-full ${data.postgres_connected ? 'bg-green-500' : 'bg-yellow-500'}`} />
        <span>Postgres {data.postgres_connected ? '연결됨' : '샘플 모드'}</span>
      </div>
      <div className="flex items-center gap-1.5">
        <span className={`w-2 h-2 rounded-full ${data.neo4j_connected ? 'bg-green-500' : 'bg-yellow-500'}`} />
        <span>Neo4j {data.neo4j_connected ? '연결됨' : '선택사항'}</span>
      </div>
    </div>
  )
}

const HEADER_H = 40
const DETAIL_H = 280
const TAB_HDR_H = 38

export default function App() {
  const { activeTab, setActiveTab, queryResponse, tableRows } = useWorkspaceStore()

  return (
    <div style={{ position: 'fixed', inset: 0, display: 'flex', flexDirection: 'column' }} className="bg-background text-foreground">
      <header
        style={{ height: HEADER_H, flexShrink: 0 }}
        className="flex items-center justify-between px-4 border-b border-border bg-card"
      >
        <div className="flex items-center gap-3">
          <span className="text-sm font-semibold tracking-tight">FabGraph</span>
          <Separator orientation="vertical" className="h-4" />
          <span className="text-xs text-muted-foreground">Hybrid-db fab analytics workspace</span>
        </div>
        <HealthBadge />
      </header>

      <div style={{ position: 'relative', flex: 1, overflow: 'hidden' }}>
        <div
          style={{ position: 'absolute', left: 0, top: 0, bottom: 0, width: '62%', display: 'flex', flexDirection: 'column', borderRight: '1px solid var(--border)' }}
          className="bg-background"
        >
          <QueryPanel />

          <div style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden', position: 'relative' }}>
            <div
              style={{ height: TAB_HDR_H, flexShrink: 0 }}
              className="flex items-center gap-0.5 px-3 border-b border-border bg-card"
            >
              {([
                { value: 'graph', label: '그래프', badge: queryResponse ? `${queryResponse.result.nodes.length}N·${queryResponse.result.edges.length}E` : null },
                { value: 'table', label: '테이블', badge: tableRows.length > 0 ? String(tableRows.length) : null },
                { value: 'chart',  label: '차트',   badge: null },
              ] as const).map(({ value, label, badge }) => (
                <button
                  key={value}
                  onClick={() => setActiveTab(value)}
                  className={`text-xs px-3 h-6 rounded transition-colors ${
                    activeTab === value
                      ? 'bg-background text-foreground font-medium shadow-sm border border-border'
                      : 'text-muted-foreground hover:text-foreground'
                  }`}
                >
                  {label}
                  {badge && <span className="ml-1 opacity-60">{badge}</span>}
                </button>
              ))}
            </div>

            <div style={{ position: 'absolute', top: TAB_HDR_H, left: 0, right: 0, bottom: DETAIL_H, overflow: 'hidden' }}>
              {activeTab === 'graph' && <GraphView />}
              {activeTab === 'table' && <TableView />}
              {activeTab === 'chart' && <ChartView />}
            </div>

            <div
              style={{ position: 'absolute', bottom: 0, left: 0, right: 0, height: DETAIL_H }}
              className="border-t border-border"
            >
              <div className="px-3 py-1.5 border-b border-border bg-muted/30">
                <span className="text-xs font-medium">상세 정보</span>
              </div>
              <div style={{ height: DETAIL_H - 30, overflow: 'auto' }}>
                <DetailPanel />
              </div>
            </div>
          </div>
        </div>

        <div
          style={{ position: 'absolute', right: 0, top: 0, bottom: 0, width: '38%' }}
          className="bg-background"
        >
          <ChatPanel />
        </div>
      </div>
    </div>
  )
}
