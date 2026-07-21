"use client"

import { useMemo, useState } from "react"
import * as XLSX from "xlsx"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Dialog } from "radix-ui"
import { DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import type { QueryResult } from "@/lib/api"
import { AlertCircleIcon, ArrowDownNarrowWide, ArrowUpNarrowWide, DownloadIcon, FilterXIcon, SearchIcon } from "lucide-react"

/** 表格中直接显示的列数上限，其余列放入点击行后的详情弹窗 */
const VISIBLE_COLUMNS = 8

interface ResultCardProps {
    result: QueryResult
}

type SortDir = "asc" | "desc" | null

function formatCell(val: unknown): string {
    if (val === null || val === undefined) return "\u2014"
    if (typeof val === "object") return JSON.stringify(val)
    return String(val)
}

function buildColumns(data: Record<string, unknown>[]): string[] {
    if (data.length === 0) return []
    return Object.keys(data[0])
}

/** 将行数据转为 CSV/Excel 友好的纯对象（拍平嵌套对象） */
function flattenRow(row: Record<string, unknown>): Record<string, unknown> {
    const flat: Record<string, unknown> = {}
    for (const [key, val] of Object.entries(row)) {
        flat[key] = val === null || val === undefined ? "" : (typeof val === "object" ? JSON.stringify(val) : val)
    }
    return flat
}

export function ResultCard({ result }: ResultCardProps) {
    const columns = buildColumns(result.data)
    const hasData = result.data.length > 0
    const [selectedRow, setSelectedRow] = useState<Record<string, unknown> | null>(null)
    const [dialogOpen, setDialogOpen] = useState(false)

    // ── 排序 ──
    const [sortColumn, setSortColumn] = useState<string | null>(null)
    const [sortDir, setSortDir] = useState<SortDir>(null)

    // ── 筛选 ──
    const [filters, setFilters] = useState<Record<string, string>>({})

    const hasMoreColumns = columns.length > VISIBLE_COLUMNS
    const visibleColumns = hasMoreColumns ? columns.slice(0, VISIBLE_COLUMNS) : columns

    // ── 数据加工：筛选 → 排序 ──
    const processedData = useMemo(() => {
        let data = result.data

        // 筛选
        const activeFilters = Object.entries(filters).filter(([, v]) => v.trim() !== "")
        if (activeFilters.length > 0) {
            data = data.filter((row) =>
                activeFilters.every(([col, val]) => {
                    const cell = formatCell(row[col]).toLowerCase()
                    return cell.includes(val.toLowerCase())
                })
            )
        }

        // 排序
        if (sortColumn && sortDir) {
            data = [...data].sort((a, b) => {
                const aVal = a[sortColumn]
                const bVal = b[sortColumn]
                // 空值排到最后
                if (aVal == null && bVal == null) return 0
                if (aVal == null) return 1
                if (bVal == null) return -1

                let cmp = 0
                if (typeof aVal === "number" && typeof bVal === "number") {
                    cmp = aVal - bVal
                } else {
                    cmp = String(aVal).localeCompare(String(bVal), "zh-CN", { numeric: true })
                }
                return sortDir === "desc" ? -cmp : cmp
            })
        }

        return data
    }, [result.data, filters, sortColumn, sortDir])

    const handleSort = (col: string) => {
        if (sortColumn !== col) {
            setSortColumn(col)
            setSortDir("asc")
        } else {
            setSortDir((prev) => (prev === "asc" ? "desc" : prev === "desc" ? null : "asc"))
            if (sortDir === "desc") setSortColumn(null)
        }
    }

    const handleFilterChange = (col: string, value: string) => {
        setFilters((prev) => {
            const next = { ...prev }
            if (value.trim() === "") {
                delete next[col]
            } else {
                next[col] = value
            }
            return next
        })
    }

    const clearFilters = () => setFilters({})

    const hasActiveFilters = Object.values(filters).some((v) => v.trim() !== "")

    // ── Excel 导出（包含全部原始列，不受 VISIBLE_COLUMNS 限制）──
    const exportToExcel = () => {
        const rows = result.data.map(flattenRow)
        const ws = XLSX.utils.json_to_sheet(rows)

        // 自动列宽
        const colWidths = columns.map((col) => {
            const maxLen = Math.max(
                col.length * 2, // 中文按 2 字符宽度估算
                ...rows.map((r) => String(r[col] ?? "").length)
            )
            return { wch: Math.min(Math.max(maxLen, 10), 60) }
        })
        ws["!cols"] = colWidths

        const wb = XLSX.utils.book_new()
        XLSX.utils.book_append_sheet(wb, ws, "明细数据")
        XLSX.writeFile(wb, `${result.name}_明细.xlsx`)
    }

    // ── 排序指示器 ──
    function SortIndicator({ column }: { column: string }) {
        if (sortColumn !== column) return null
        return sortDir === "asc" ? (
            <ArrowUpNarrowWide className="ml-0.5 inline size-3" />
        ) : (
            <ArrowDownNarrowWide className="ml-0.5 inline size-3" />
        )
    }

    // --- Error only (no data) ---
    if (result.error && !hasData) {
        return (
            <Card>
                <CardContent className="flex items-center gap-3 py-6">
                    <AlertCircleIcon className="size-4 shrink-0 text-destructive" />
                    <div className="min-w-0">
                        <div className="truncate text-sm font-medium text-destructive">{result.name}</div>
                        <div className="truncate text-xs text-muted-foreground">{result.error}</div>
                    </div>
                </CardContent>
            </Card>
        )
    }

    // --- Empty ---
    if (!hasData) {
        return (
            <Card>
                <CardContent className="flex flex-col items-center gap-1 py-10 text-center">
                    <p className="text-xs font-medium">{result.name}</p>
                    <p className="text-xs text-muted-foreground">无匹配结果</p>
                </CardContent>
            </Card>
        )
    }

    // --- Has data ---
    const sortBtnCls =
        "inline-flex items-center gap-0.5 whitespace-nowrap rounded px-1 -mx-1 py-0 transition-colors hover:bg-accent/50 cursor-pointer select-none"

    return (
        <>
            {/* 工具栏 */}
            <div className="mb-2 flex items-center gap-2">
                <span className="text-xs text-muted-foreground">
                    {processedData.length} / {result.data.length} 行
                    {hasActiveFilters && (
                        <button onClick={clearFilters} className="ml-2 inline-flex items-center gap-0.5 text-xs text-primary hover:underline">
                            <FilterXIcon className="size-3" />
                            清除筛选
                        </button>
                    )}
                </span>
                <div className="flex-1" />
                <Button variant="outline" size="sm" onClick={exportToExcel}>
                    <DownloadIcon className="mr-1 size-3.5" />
                    导出 Excel
                </Button>
            </div>

            {/* 表格 */}
            <div className="max-h-[75vh] overflow-auto rounded-md border">
                <Table>
                    <TableHeader className="sticky top-0 z-20 bg-background">
                        {/* 第 1 行：列名 + 排序 */}
                        <TableRow>
                            <TableHead className="sticky left-0 z-30 w-10 bg-background px-2 text-muted-foreground">#</TableHead>
                            {visibleColumns.map((col) => (
                                <TableHead key={col} className="px-2">
                                    <span className={sortBtnCls} onClick={() => handleSort(col)} title={sortDir ? `切换排序方向` : `点击升序`}>
                                        {col}
                                        <SortIndicator column={col} />
                                    </span>
                                </TableHead>
                            ))}
                        </TableRow>
                        {/* 第 2 行：筛选输入框 */}
                        <TableRow>
                            <TableHead className="sticky left-0 z-30 bg-background px-2" />
                            {visibleColumns.map((col) => (
                                <TableHead key={col} className="px-1 py-1">
                                    <div className="relative">
                                        <SearchIcon className="pointer-events-none absolute left-1.5 top-1/2 size-3 -translate-y-1/2 text-muted-foreground/40" />
                                        <Input
                                            placeholder="筛选..."
                                            value={filters[col] ?? ""}
                                            onChange={(e) => handleFilterChange(col, e.target.value)}
                                            className="h-7 rounded pl-6 text-[0.7rem]"
                                        />
                                    </div>
                                </TableHead>
                            ))}
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {processedData.length === 0 ? (
                            <TableRow>
                                <TableCell colSpan={visibleColumns.length + 1} className="py-12 text-center text-sm text-muted-foreground">
                                    无匹配数据
                                </TableCell>
                            </TableRow>
                        ) : (
                            processedData.map((row, i) => (
                                <TableRow
                                    key={i}
                                    className={hasMoreColumns ? "cursor-pointer" : undefined}
                                    onClick={() => {
                                        if (hasMoreColumns) {
                                            setSelectedRow(row)
                                            setDialogOpen(true)
                                        }
                                    }}
                                >
                                    <TableCell className="sticky left-0 z-20 bg-background px-2 text-muted-foreground">{i + 1}</TableCell>
                                    {visibleColumns.map((col) => (
                                        <TableCell key={col} className="max-w-60 truncate px-2" title={formatCell(row[col])}>
                                            {formatCell(row[col])}
                                        </TableCell>
                                    ))}
                                </TableRow>
                            ))
                        )}
                    </TableBody>
                </Table>
            </div>

            {/* Detail dialog — only when there are extra columns */}
            {hasMoreColumns && (
                <Dialog.Root open={dialogOpen} onOpenChange={setDialogOpen}>
                    <DialogContent>
                        <DialogHeader>
                            <DialogTitle>
                                行详情
                                <span className="ml-2 text-xs font-normal text-muted-foreground">
                                    {columns.length} 列
                                </span>
                            </DialogTitle>
                        </DialogHeader>
                        <div className="max-h-[65vh] overflow-y-auto">
                            <table className="w-full text-xs">
                                <tbody>
                                    {columns.map((col, idx) => (
                                        <tr
                                            key={col}
                                            className={
                                                "border-b border-border last:border-0 " +
                                                (idx % 2 === 0 ? "bg-background" : "bg-muted/20")
                                            }
                                        >
                                            <td className="w-48 shrink-0 px-3 py-2.5 font-medium text-muted-foreground">
                                                {col}
                                            </td>
                                            <td className="break-all px-3 py-2.5">
                                                {selectedRow ? formatCell(selectedRow[col]) : "\u2014"}
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </DialogContent>
                </Dialog.Root>
            )}
        </>
    )
}
