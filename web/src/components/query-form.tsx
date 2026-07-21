"use client"

import { useEffect, useRef, useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Checkbox } from "@/components/ui/checkbox"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { type QueryName, type QueryOption, type QueryRequest, fetchProjectCodes, fetchProcessCodes, fetchMaterialCodes, type ProjectCode } from "@/lib/api"
import { GitCompareArrowsIcon, SearchIcon, ShieldCheckIcon } from "lucide-react"

interface QueryFormProps {
    formValues: QueryRequest
    onFormChange: (values: QueryRequest) => void
    onSubmit: () => void
    onReworkClick?: () => void
    onDiagnoseClick?: () => void
    loading: boolean
    diagnoseLoading?: boolean
    selectedQueries: QueryName[]
    onSelectedQueriesChange: (queries: QueryName[]) => void
    queryOptions: QueryOption[]
}

/** 快捷分组方案 — 基于 query value 前缀匹配 */
const PRESETS: { id: string; label: string; match: (value: string) => boolean }[] = [
    { id: "all", label: "全选", match: () => true },
    { id: "cgmes_eas", label: "城轨MES+EAS", match: (v) => v.startsWith("cgmes_") || v.startsWith("eas_") },
    { id: "eas", label: "EAS", match: (v) => v.startsWith("eas_") },
    { id: "cgmes", label: "城轨MES", match: (v) => v.startsWith("cgmes_") },
]

// ── 带自动补全的输入框组件 ────────────────────────────────────────────
interface AutoCompleteInputProps {
    id: string
    label: string
    placeholder: string
    value: string
    onChange: (value: string) => void
    /** 根据输入获取候选项列表 */
    fetchSuggestions: (query: string) => Promise<(string | { label: string; value: string })[]>
    /** 选中候选项时的回调 */
    onSelect: (selected: string | { label: string; value: string }) => void
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
    const [suggestions, setSuggestions] = useState<(string | { label: string; value: string })[]>([])
    const [open, setOpen] = useState(false)
    const [highlightIndex, setHighlightIndex] = useState(-1)
    const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null)
    const wrapperRef = useRef<HTMLDivElement>(null)

    // 点击外部关闭下拉
    useEffect(() => {
        function handleClickOutside(e: MouseEvent) {
            if (wrapperRef.current && !wrapperRef.current.contains(e.target as Node)) {
                setOpen(false)
            }
        }
        document.addEventListener("mousedown", handleClickOutside)
        return () => document.removeEventListener("mousedown", handleClickOutside)
    }, [])

    function handleInput(val: string) {
        setHighlightIndex(-1)
        onChange(val) // 将用户输入实时同步到父组件 formValues

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

    function handleSelect(item: string | { label: string; value: string }) {
        if (timerRef.current) clearTimeout(timerRef.current)
        onSelect(item)
        setSuggestions([])
        setOpen(false)
    }

    function handleKeyDown(e: React.KeyboardEvent) {
        if (!open || suggestions.length === 0) return
        if (e.key === "ArrowDown") {
            e.preventDefault()
            setHighlightIndex((prev) => (prev < suggestions.length - 1 ? prev + 1 : 0))
        } else if (e.key === "ArrowUp") {
            e.preventDefault()
            setHighlightIndex((prev) => (prev > 0 ? prev - 1 : suggestions.length - 1))
        } else if (e.key === "Enter" && highlightIndex >= 0) {
            e.preventDefault()
            handleSelect(suggestions[highlightIndex])
        } else if (e.key === "Escape") {
            setOpen(false)
        }
    }

    const displayValue = (item: string | { label: string; value: string }) =>
        typeof item === "string" ? item : item.label

    return (
        <div className="flex min-w-45 flex-1 flex-col gap-1 relative" ref={wrapperRef}>
            <Label htmlFor={id}>{label}</Label>
            <Input
                id={id}
                placeholder={placeholder}
                value={value}
                onChange={(e) => handleInput(e.target.value)}
                onKeyDown={handleKeyDown}
                onFocus={() => { if (suggestions.length > 0) setOpen(true) }}
            />
            {open && suggestions.length > 0 && (
                <ul className="absolute top-full left-0 right-0 z-50 mt-0.5 max-h-48 overflow-auto rounded-md border bg-popover p-1 text-xs shadow-md">
                    {suggestions.map((item, i) => (
                        <li
                            key={i}
                            className={`cursor-pointer rounded-sm px-2 py-1.5 ${i === highlightIndex ? "bg-accent text-accent-foreground" : ""}`}
                            onMouseDown={() => handleSelect(item)}
                            onMouseEnter={() => setHighlightIndex(i)}
                        >
                            {displayValue(item)}
                        </li>
                    ))}
                </ul>
            )}
        </div>
    )
}

export function QueryForm({ formValues, onFormChange, onSubmit, onReworkClick, onDiagnoseClick, loading, diagnoseLoading, selectedQueries, onSelectedQueriesChange, queryOptions }: QueryFormProps) {
    const [activePreset, setActivePreset] = useState<string | null>(null)

    function updateField(field: keyof QueryRequest, value: string) {
        if (field === "track_number") {
            const num = value === "" ? null : Number(value)
            onFormChange({
                ...formValues,
                [field]: isNaN(num as number) ? null : num,
            })
        } else {
            onFormChange({ ...formValues, [field]: value || null })
        }
    }

    function toggleQuery(queryName: QueryName) {
        setActivePreset(null)
        if (selectedQueries.includes(queryName)) {
            onSelectedQueriesChange(selectedQueries.filter((q) => q !== queryName))
        } else {
            onSelectedQueriesChange([...selectedQueries, queryName])
        }
    }

    function applyPreset(presetId: string) {
        const preset = PRESETS.find((p) => p.id === presetId)
        if (!preset) return

        if (activePreset === presetId) {
            setActivePreset(null)
            onSelectedQueriesChange([])
        } else {
            setActivePreset(presetId)
            const groupValues = queryOptions
                .filter((o) => preset.match(o.value))
                .map((o) => o.value)
            onSelectedQueriesChange(groupValues)
        }
    }

    // 工序编码自动补全：根据输入的 工序名称 模糊匹配
    async function fetchProcessSuggestions(query: string): Promise<{ label: string; value: string }[]> {
        const codes = await fetchProcessCodes(query)
        return codes.map((p) => ({
            label: `${p.工序编码} - ${p.工序名称}`,
            value: p.工序编码,
        }))
    }

    // 项目号自动补全：根据输入的 项目名称 模糊匹配
    async function fetchProjectSuggestions(query: string): Promise<{ label: string; value: string }[]> {
        const projects = await fetchProjectCodes(query)
        return projects.map((p: ProjectCode) => ({
            label: `${p.项目号} - ${p.项目名称}`,
            value: p.项目号,
        }))
    }

    // 物料编码自动补全：根据输入的 物料名称 模糊匹配
    async function fetchMaterialSuggestions(query: string): Promise<{ label: string; value: string }[]> {
        const codes = await fetchMaterialCodes(query)
        return codes.map((m) => ({
            label: `${m.物料编码} - ${m.物料名称}`,
            value: m.物料编码,
        }))
    }

    return (
        <form
            onSubmit={(e) => {
                e.preventDefault()
                onSubmit()
            }}
            className="grid grid-cols-1 gap-3 md:grid-cols-[auto_1fr]"
        >
            {/* ─── 左侧：查询目标 ─── */}
            <Card className="shrink-0">
                <CardHeader>
                    <CardTitle>查询目标</CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="flex flex-col gap-3">
                        <div className="flex gap-3">
                            <div className="flex w-36 shrink-0 flex-col gap-1.5">
                                <span className="text-[0.65rem] font-medium uppercase tracking-wider text-muted-foreground">
                                    快捷方案
                                </span>
                                <div className="flex flex-col gap-1.5">
                                    {PRESETS.map((p) => (
                                        <div key={p.id} className="flex items-center gap-2">
                                            <Checkbox
                                                id={`preset-${p.id}`}
                                                checked={activePreset === p.id}
                                                onCheckedChange={() => applyPreset(p.id)}
                                            />
                                            <label
                                                htmlFor={`preset-${p.id}`}
                                                className="cursor-pointer text-sm select-none leading-tight"
                                            >
                                                {p.label}
                                            </label>
                                        </div>
                                    ))}
                                </div>
                            </div>

                            <div className="flex min-w-0 flex-1 flex-col gap-1.5">
                                <span className="text-[0.65rem] font-medium uppercase tracking-wider text-muted-foreground">
                                    全部项目
                                </span>
                                <div className="grid grid-cols-1 gap-x-3 gap-y-1.5 xl:grid-cols-3">
                                    {queryOptions.map((opt) => (
                                        <div key={opt.value} className="flex items-center gap-2">
                                            <Checkbox
                                                id={`query-${opt.value}`}
                                                checked={selectedQueries.includes(opt.value)}
                                                onCheckedChange={() => toggleQuery(opt.value)}
                                            />
                                            <label
                                                htmlFor={`query-${opt.value}`}
                                                className="cursor-pointer text-sm select-none leading-tight whitespace-nowrap"
                                            >
                                                {opt.label}
                                            </label>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </div>

                        <div className="text-xs text-muted-foreground">
                            已选 {selectedQueries.length} / {queryOptions.length} 项
                        </div>
                    </div>
                </CardContent>
            </Card>

            {/* ─── 右侧：筛选条件 + 查询按钮 ─── */}
            <Card className="min-w-0 flex-1">
                <CardHeader>
                    <CardTitle>筛选条件</CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="flex flex-col gap-3">
                        <div className="flex flex-wrap gap-3">
                            {/* 项目号 — 带自动补全 */}
                            <AutoCompleteInput
                                id="project"
                                label="项目号"
                                placeholder="输入项目名称搜索..."
                                value={formValues.project ?? ""}
                                onChange={(val) => updateField("project", val)}
                                fetchSuggestions={fetchProjectSuggestions}
                                onSelect={(item) => {
                                    const v = typeof item === "string" ? item : item.value
                                    updateField("project", v)
                                }}
                            />

                            <div className="flex min-w-45 flex-1 flex-col gap-1">
                                <Label htmlFor="track_number">车号</Label>
                                <Input
                                    id="track_number"
                                    type="number"
                                    placeholder="例: 18"
                                    value={formValues.track_number ?? ""}
                                    onChange={(e) => updateField("track_number", e.target.value)}
                                />
                            </div>
                            <div className="flex min-w-45 flex-1 flex-col gap-1">
                                <Label htmlFor="jch_num">节车号</Label>
                                <Input
                                    id="jch_num"
                                    placeholder="例: Tc1"
                                    value={formValues.jch_num ?? ""}
                                    onChange={(e) => updateField("jch_num", e.target.value)}
                                />
                            </div>

                            {/* 工序编码 — 带自动补全 */}
                            <AutoCompleteInput
                                id="process"
                                label="工序编码"
                                placeholder="输入工序名称搜索..."
                                value={formValues.process ?? ""}
                                onChange={(val) => updateField("process", val)}
                                fetchSuggestions={fetchProcessSuggestions}
                                onSelect={(item) => {
                                    const v = typeof item === "string" ? item : item.value
                                    updateField("process", v)
                                }}
                            />

                            {/* 物料编码 — 带自动补全 */}
                            <AutoCompleteInput
                                id="material"
                                label="物料编码"
                                placeholder="输入物料名称搜索..."
                                value={formValues.material ?? ""}
                                onChange={(val) => updateField("material", val)}
                                fetchSuggestions={fetchMaterialSuggestions}
                                onSelect={(item) => {
                                    const v = typeof item === "string" ? item : item.value
                                    updateField("material", v)
                                }}
                            />
                            <div className="flex min-w-45 flex-1 flex-col gap-1">
                                <Label htmlFor="order_code">生产订单编码</Label>
                                <Input
                                    id="order_code"
                                    placeholder="例: MO24070001"
                                    value={formValues.order_code ?? ""}
                                    onChange={(e) => updateField("order_code", e.target.value)}
                                />
                            </div>
                        </div>

                        <div className="flex justify-end gap-2 pt-1">
                            {onReworkClick && (
                                <Button type="button" variant="outline" size="default" onClick={onReworkClick}>
                                    <span className="flex items-center gap-1.5">
                                        <GitCompareArrowsIcon className="size-3.5" />
                                        返工流程分析
                                    </span>
                                </Button>
                            )}
                            {onDiagnoseClick && (
                                <Button type="button" variant="outline" size="default" onClick={onDiagnoseClick} disabled={diagnoseLoading}>
                                    <span className="flex items-center gap-1.5">
                                        <ShieldCheckIcon className="size-3.5" />
                                        {diagnoseLoading ? "诊断中..." : "bomID一致性诊断"}
                                    </span>
                                </Button>
                            )}
                            <Button type="submit" disabled={loading || selectedQueries.length === 0} size="default">
                                {loading ? (
                                    <span className="flex items-center gap-1.5">
                                        <span className="size-3 animate-spin rounded-full border-2 border-current border-t-transparent" />
                                        查询中...
                                    </span>
                                ) : (
                                    <span className="flex items-center gap-1.5">
                                        <SearchIcon className="size-3.5" />
                                        查询
                                    </span>
                                )}
                            </Button>
                        </div>
                    </div>
                </CardContent>
            </Card>
        </form>
    )
}
