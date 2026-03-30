import { useState, useEffect } from 'react'
import { ChevronDown, ChevronUp, Play, Loader2, Database } from 'lucide-react'
import { Button } from '@/shared/ui/button'
import { Textarea } from '@/shared/ui/textarea'
import { Badge } from '@/shared/ui/badge'
import { useWorkspaceStore } from '@/store/useWorkspaceStore'
import { executeQuery } from '@/shared/api/client'

const PRESET_QUERIES = [
  {
    label: 'UC1 최신 Wafer',
    query: '// uc1 latest wafers\nMATCH (w:Wafer)-[:BELONGS_TO]->(l:Lot)-[:USES_RECIPE]->(r:Recipe) RETURN w, l, r ORDER BY w.created_at DESC LIMIT 10',
  },
  {
    label: 'UC2 조건 + 통계',
    query: '// uc2 filtered wafers\nMATCH (w:Wafer)-[:BELONGS_TO]->(l:Lot)-[:USES_RECIPE]->(r:Recipe) RETURN w, l, r // filtered wafer slice',
  },
  {
    label: 'UC3 동일기간 그룹',
    query: '// uc3 same period DOE exploration\nMATCH (w:Wafer)-[:BELONGS_TO]->(l:Lot)-[:USES_RECIPE]->(r:Recipe) RETURN w, l, r // grouped exploration',
  },
]

function detectUseCase(query: string): string {
  const normalized = query.toLowerCase()
  if (normalized.includes('uc3') || normalized.includes('same period') || normalized.includes('doe')) return 'UC3 · Same-period Group Exploration'
  if (normalized.includes('uc2') || normalized.includes('filtered')) return 'UC2 · Conditional Filter + Statistics'
  return 'UC1 · Latest Wafers'
}

export function QueryPanel() {
  const {
    currentQuery,
    setCurrentQuery,
    isQueryPanelCollapsed,
    toggleQueryPanel,
    isQueryRunning,
    setQueryRunning,
    setQueryResponse,
    setGraphResult,
    setTableRows,
    setActiveTab,
    activeFilters,
    setChartConfig,
  } = useWorkspaceStore()

  const [localQuery, setLocalQuery] = useState(currentQuery || PRESET_QUERIES[0].query)

  useEffect(() => {
    setLocalQuery(currentQuery || PRESET_QUERIES[0].query)
  }, [currentQuery])

  async function handleRun() {
    const trimmed = localQuery.trim()
    if (!trimmed || isQueryRunning) return

    setCurrentQuery(trimmed)
    setQueryRunning(true)
    try {
      const res = await executeQuery(trimmed)
      setQueryResponse(res)
      setGraphResult(res.result)
      setTableRows(res.result.raw)
      if (trimmed.toLowerCase().includes('uc2') || trimmed.toLowerCase().includes('uc3')) {
        setChartConfig({ chartType: 'bar', xKey: trimmed.toLowerCase().includes('uc3') ? 'group_key' : 'wafer_id' })
      }
      setActiveTab(res.result.nodes.length > 0 ? 'graph' : 'table')
    } catch (err) {
      console.error('쿼리 실행 오류:', err)
    } finally {
      setQueryRunning(false)
    }
  }

  function handlePreset(query: string) {
    setLocalQuery(query)
    setCurrentQuery(query)
  }

  function handleKeyDown(e: React.KeyboardEvent<HTMLTextAreaElement>) {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      e.preventDefault()
      void handleRun()
    }
  }

  const filterCount = Object.keys(activeFilters).length
  const title = detectUseCase(localQuery || currentQuery)

  if (isQueryPanelCollapsed) {
    return (
      <div className="flex items-center gap-2 px-3 py-2 bg-card border-b border-border">
        <Database className="w-4 h-4 text-muted-foreground shrink-0" />
        <span className="text-xs text-muted-foreground truncate flex-1">
          {currentQuery || '쿼리 없음'}
        </span>
        {filterCount > 0 && (
          <Badge variant="secondary" className="text-xs">
            필터 {filterCount}
          </Badge>
        )}
        {isQueryRunning && <Loader2 className="w-4 h-4 animate-spin text-primary" />}
        <Button variant="ghost" size="icon" className="h-6 w-6" onClick={toggleQueryPanel}>
          <ChevronDown className="w-4 h-4" />
        </Button>
      </div>
    )
  }

  return (
    <div className="bg-card border-b border-border">
      <div className="flex items-center justify-between px-3 py-2 border-b border-border">
        <div className="flex items-center gap-2">
          <Database className="w-4 h-4 text-muted-foreground" />
          <span className="text-sm font-medium">{title}</span>
          {filterCount > 0 && (
            <Badge variant="secondary" className="text-xs">
              필터 {filterCount}
            </Badge>
          )}
        </div>
        <Button variant="ghost" size="icon" className="h-6 w-6" onClick={toggleQueryPanel}>
          <ChevronUp className="w-4 h-4" />
        </Button>
      </div>

      <div className="flex items-start justify-between gap-2 px-3 pt-2">
        <div className="flex flex-wrap gap-1">
          {PRESET_QUERIES.map((p) => (
            <Button
              key={p.label}
              variant="outline"
              size="sm"
              className="h-6 text-xs px-2"
              onClick={() => handlePreset(p.query)}
            >
              {p.label}
            </Button>
          ))}
        </div>
        <Button
          size="sm"
          className="h-7 text-xs gap-1 shrink-0"
          onClick={() => void handleRun()}
          disabled={isQueryRunning || !localQuery.trim()}
        >
          {isQueryRunning ? (
            <Loader2 className="w-3 h-3 animate-spin" />
          ) : (
            <Play className="w-3 h-3" />
          )}
          실행
        </Button>
      </div>

      <div className="px-3 pt-2 pb-1">
        <p className="text-[11px] text-muted-foreground">
          UC1 최신 조회 / UC2 조건 필터+통계 / UC3 동일기간 그룹 탐색용 프리셋입니다.
        </p>
      </div>

      <div className="px-3 pt-2 pb-3">
        <Textarea
          value={localQuery}
          onChange={(e) => setLocalQuery(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Cypher 스타일 쿼리를 입력하세요 (Ctrl+Enter 실행)"
          className="font-mono text-xs min-h-[80px] resize-none bg-muted/30"
          spellCheck={false}
        />
      </div>
    </div>
  )
}
