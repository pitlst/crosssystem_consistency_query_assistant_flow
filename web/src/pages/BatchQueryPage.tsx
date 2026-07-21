import { useCallback, useEffect, useMemo, useState } from 'react'
import { useLocation } from 'react-router-dom'
import { QueryForm } from '@/components/query-form'
import { ResultCard } from '@/components/result-table'
import { Badge } from '@/components/ui/badge'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import {
  batchExecute,
  fetchQueryOptions,
  type QueryName,
  type QueryOption,
  type QueryRequest,
  type QueryResult,
} from '@/lib/api'
import { DatabaseIcon } from 'lucide-react'

export default function BatchQueryPage() {
  const location = useLocation()
  const [formValues, setFormValues] = useState<QueryRequest>({
    project: null,
    track_number: null,
    jch_num: null,
    process: null,
    material: null,
  })
  const [results, setResults] = useState<QueryResult[] | null>(null)
  const [activeTab, setActiveTab] = useState<string>('')
  const [loading, setLoading] = useState(false)
  const [queryOptions, setQueryOptions] = useState<QueryOption[]>([])
  const [selectedQueries, setSelectedQueries] = useState<QueryName[]>([])

  useEffect(() => {
    const state = location.state as Partial<QueryRequest> | null
    if (state && Object.keys(state).length > 0) {
      setFormValues((prev) => ({ ...prev, ...state }))
    }
  }, [location.state])

  useEffect(() => {
    fetchQueryOptions().then((opts) => {
      setQueryOptions(opts)
      setSelectedQueries(
        opts.filter((o) => o.value.startsWith('cgmes_') || o.value.startsWith('eas_')).map((o) => o.value),
      )
    })
  }, [])

  const sortedResults = useMemo(() => {
    if (!results) return null
    const orderMap = new Map(queryOptions.map((o, i) => [o.value, i]))
    return [...results]
      .filter((r) => selectedQueries.includes(r.name))
      .sort((a, b) => (orderMap.get(a.name) ?? 99) - (orderMap.get(b.name) ?? 99))
  }, [results, queryOptions, selectedQueries])

  const handleSubmit = useCallback(async () => {
    if (
      !formValues.project &&
      formValues.track_number == null &&
      !formValues.jch_num &&
      !formValues.process &&
      !formValues.material &&
      !formValues.order_code
    ) {
      alert('请至少填写一个筛选条件后再查询')
      return
    }

    setLoading(true)
    setResults(null)
    setActiveTab('')
    try {
      const next = await batchExecute(selectedQueries, formValues)
      setResults(next)
      if (next.length > 0) setActiveTab(next[0].name)
    } catch (err) {
      alert(err instanceof Error ? err.message : String(err))
    } finally {
      setLoading(false)
    }
  }, [formValues, selectedQueries])

  return (
    <div className="flex flex-col gap-4">
      <QueryForm
        formValues={formValues}
        onFormChange={setFormValues}
        onSubmit={handleSubmit}
        loading={loading}
        selectedQueries={selectedQueries}
        onSelectedQueriesChange={setSelectedQueries}
        queryOptions={queryOptions}
      />

      {loading && (!results || results.length === 0) && (
        <div className="flex items-center justify-center py-16">
          <div className="flex items-center gap-2 text-muted-foreground">
            <span className="size-4 animate-spin rounded-full border-2 border-primary border-t-transparent" />
            正在并发查询 {selectedQueries.length} 个数据源...
          </div>
        </div>
      )}

      {sortedResults && sortedResults.length > 0 ? (
        <Tabs value={activeTab} onValueChange={setActiveTab} orientation="vertical" className="flex-1">
          <div className="flex w-60 shrink-0 flex-col gap-3 self-start">
            <Card>
              <CardHeader>
                <CardTitle>查询结果页签</CardTitle>
              </CardHeader>
              <CardContent className="px-3 pb-3">
                <TabsList className="w-full">
                  {sortedResults.map((r) => {
                    const option = queryOptions.find((o) => o.value === r.name)
                    const label = option?.label ?? r.name
                    const hasError = !!r.error
                    const rowCount = r.data.length
                    return (
                      <TabsTrigger key={r.name} value={r.name} className="gap-1.5">
                        <span className="min-w-0 truncate">{label}</span>
                        {hasError && rowCount === 0 ? (
                          <Badge variant="destructive" className="ml-auto h-4 min-w-4 px-1 text-[0.6rem] leading-none">
                            !
                          </Badge>
                        ) : (
                          <Badge variant="secondary" className="ml-auto h-4 min-w-4 px-1 text-[0.6rem] leading-none">
                            {rowCount}
                          </Badge>
                        )}
                      </TabsTrigger>
                    )
                  })}
                </TabsList>
              </CardContent>
            </Card>
          </div>

          {sortedResults.map((r) => (
            <TabsContent key={r.name} value={r.name}>
              <ResultCard result={r} />
            </TabsContent>
          ))}
        </Tabs>
      ) : null}

      {!loading && !results && (
        <div className="flex flex-col items-center gap-2 py-16 text-center">
          <DatabaseIcon className="size-8 text-muted-foreground/30" />
          <p className="text-sm text-muted-foreground">请填写筛选条件并点击查询</p>
        </div>
      )}
    </div>
  )
}
