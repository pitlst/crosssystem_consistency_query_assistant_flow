import { FlowCanvas } from '@/components/flow-canvas'
import { Workflow } from 'lucide-react'

export default function FlowPage() {
  return (
    <div className="flex flex-col gap-4">
      <div className="flex items-center gap-2">
        <Workflow className="size-5 text-muted-foreground" />
        <div>
          <h1 className="text-lg font-semibold">动态上下查节点图</h1>
          <p className="text-xs text-muted-foreground">
            从左侧添加预制 query 节点，连线映射字段，配置常量筛选后执行。
          </p>
        </div>
      </div>
      <FlowCanvas />
    </div>
  )
}
