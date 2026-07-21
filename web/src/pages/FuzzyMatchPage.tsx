import { useEffect, useRef, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import {
  fetchMaterialCodes,
  fetchProcessCodes,
  fetchProjectCodes,
  type MaterialCode,
  type ProcessCode,
  type ProjectCode,
} from '@/lib/api'
import { ArrowRightIcon } from 'lucide-react'

interface AutoCompleteInputProps {
  id: string
  label: string
  placeholder: string
  value: string
  onChange: (value: string) => void
  fetchSuggestions: (query: string) => Promise<{ label: string; value: string }[]>
  onSelect: (selected: { label: string; value: string }) => void
}

function AutoCompleteInput({
  id,
  label,
  placeholder,
  value,
  onChange,
  fetchSuggestions,
  onSelect,
}: AutoCompleteInputProps) {
  const [suggestions, setSuggestions] = useState<{ label: string; value: string }[]>([])
  const [open, setOpen] = useState(false)
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null)
  const wrapperRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (wrapperRef.current && !wrapperRef.current.contains(e.target as Node)) {
        setOpen(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  function handleInput(val: string) {
    onChange(val)
    if (timerRef.current) clearTimeout(timerRef.current)
    if (!val.trim()) {
      setSuggestions([])
      setOpen(false)
      return
    }
    timerRef.current = setTimeout(async () => {
      const results = await fetchSuggestions(val)
      setSuggestions(results)
      setOpen(results.length > 0)
    }, 250)
  }

  return (
    <div className="relative flex flex-col gap-1" ref={wrapperRef}>
      <Label htmlFor={id}>{label}</Label>
      <Input
        id={id}
        placeholder={placeholder}
        value={value}
        onChange={(e) => handleInput(e.target.value)}
        onFocus={() => {
          if (suggestions.length > 0) setOpen(true)
        }}
      />
      {open && suggestions.length > 0 && (
        <ul className="absolute top-full z-50 mt-0.5 max-h-48 w-full overflow-auto rounded-md border bg-popover p-1 text-xs shadow-md">
          {suggestions.map((item) => (
            <li
              key={item.value}
              className="cursor-pointer rounded-sm px-2 py-1.5 hover:bg-accent hover:text-accent-foreground"
              onMouseDown={() => {
                onSelect(item)
                setOpen(false)
              }}
            >
              {item.label}
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}

function ResultList({ title, rows }: { title: string; rows: string[] }) {
  return (
    <div className="rounded-md border bg-muted/20 p-3">
      <div className="mb-2 text-xs font-medium text-muted-foreground">{title}</div>
      {rows.length === 0 ? (
        <p className="text-xs text-muted-foreground">暂无匹配结果</p>
      ) : (
        <ul className="space-y-1 text-sm">
          {rows.map((row) => (
            <li key={row} className="rounded bg-background px-2 py-1">
              {row}
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}

export default function FuzzyMatchPage() {
  const navigate = useNavigate()
  const [projectQuery, setProjectQuery] = useState('')
  const [processQuery, setProcessQuery] = useState('')
  const [materialQuery, setMaterialQuery] = useState('')
  const [projectResults, setProjectResults] = useState<string[]>([])
  const [processResults, setProcessResults] = useState<string[]>([])
  const [materialResults, setMaterialResults] = useState<string[]>([])
  const [selectedProject, setSelectedProject] = useState('')
  const [selectedProcess, setSelectedProcess] = useState('')
  const [selectedMaterial, setSelectedMaterial] = useState('')

  async function searchProjects() {
    const rows = await fetchProjectCodes(projectQuery)
    setProjectResults(rows.map((p: ProjectCode) => `${p.项目号} - ${p.项目名称}`))
  }

  async function searchProcesses() {
    const rows = await fetchProcessCodes(processQuery)
    setProcessResults(rows.map((p: ProcessCode) => `${p.工序编码} - ${p.工序名称}`))
  }

  async function searchMaterials() {
    const rows = await fetchMaterialCodes(materialQuery)
    setMaterialResults(rows.map((m: MaterialCode) => `${m.物料编码} - ${m.物料名称}`))
  }

  function applyToBatchQuery() {
    navigate('/batch', {
      state: {
        project: selectedProject || undefined,
        process: selectedProcess || undefined,
        material: selectedMaterial || undefined,
      },
    })
  }

  return (
    <div className="flex flex-col gap-4">
      <div className="grid grid-cols-1 gap-4 xl:grid-cols-3">
        <Card>
          <CardHeader>
            <CardTitle>项目名称 → 项目号</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <AutoCompleteInput
              id="project-name"
              label="项目名称"
              placeholder="输入项目名称搜索..."
              value={projectQuery}
              onChange={setProjectQuery}
              fetchSuggestions={async (query) => {
                const rows = await fetchProjectCodes(query)
                return rows.map((p) => ({ label: `${p.项目号} - ${p.项目名称}`, value: p.项目号 }))
              }}
              onSelect={(item) => {
                setProjectQuery(item.label)
                setSelectedProject(item.value)
                setProjectResults([item.label])
              }}
            />
            <Button type="button" variant="outline" onClick={searchProjects}>
              搜索项目号
            </Button>
            <ResultList title="匹配项目" rows={projectResults} />
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>工序名称 → 工序编码</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <AutoCompleteInput
              id="process-name"
              label="工序名称"
              placeholder="输入工序名称搜索..."
              value={processQuery}
              onChange={setProcessQuery}
              fetchSuggestions={async (query) => {
                const rows = await fetchProcessCodes(query)
                return rows.map((p) => ({ label: `${p.工序编码} - ${p.工序名称}`, value: p.工序编码 }))
              }}
              onSelect={(item) => {
                setProcessQuery(item.label)
                setSelectedProcess(item.value)
                setProcessResults([item.label])
              }}
            />
            <Button type="button" variant="outline" onClick={searchProcesses}>
              搜索工序编码
            </Button>
            <ResultList title="匹配工序" rows={processResults} />
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>物料名称 → 物料编码</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <AutoCompleteInput
              id="material-name"
              label="物料名称"
              placeholder="输入物料名称搜索..."
              value={materialQuery}
              onChange={setMaterialQuery}
              fetchSuggestions={async (query) => {
                const rows = await fetchMaterialCodes(query)
                return rows.map((m) => ({ label: `${m.物料编码} - ${m.物料名称}`, value: m.物料编码 }))
              }}
              onSelect={(item) => {
                setMaterialQuery(item.label)
                setSelectedMaterial(item.value)
                setMaterialResults([item.label])
              }}
            />
            <Button type="button" variant="outline" onClick={searchMaterials}>
              搜索物料编码
            </Button>
            <ResultList title="匹配物料" rows={materialResults} />
          </CardContent>
        </Card>
      </div>

      <div className="flex justify-end">
        <Button type="button" onClick={applyToBatchQuery}>
          <ArrowRightIcon className="mr-1.5 size-3.5" />
          应用到批量查询
        </Button>
      </div>
    </div>
  )
}
