import { useCallback, useEffect, useMemo, useState } from 'react'
import {
  Background,
  Controls,
  Handle,
  MiniMap,
  Position,
  ReactFlow,
  addEdge,
  useEdgesState,
  useNodesState,
  type Connection,
  type Edge,
  type Node,
  type NodeProps,
} from '@xyflow/react'
import '@xyflow/react/dist/style.css'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Badge } from '@/components/ui/badge'
import {
  fetchRegistry,
  graphExecute,
  type GraphExecuteResponse,
  type NodeTypeDefinition,
} from '@/lib/api'
import { PlayIcon, PlusIcon } from 'lucide-react'

type FlowNodeData = {
  nodeTypeId: string
  label: string
  category: string
  supportedFilters: string[]
  constInputs: Record<string, string>
}

type FlowEdgeData = {
  sourceField: string
  targetInput: string
}

function QueryFlowNode({ data, selected }: NodeProps<Node<FlowNodeData>>) {
  return (
    <div
      className={`min-w-[220px] rounded-md border bg-card px-3 py-2 shadow-sm ${selected ? 'ring-2 ring-primary' : ''}`}
    >
      <Handle type="target" position={Position.Left} className="!bg-primary" />
      <div className="text-[10px] uppercase tracking-wide text-muted-foreground">{data.category}</div>
      <div className="text-sm font-medium leading-tight">{data.label}</div>
      <div className="mt-1 text-[10px] text-muted-foreground">{data.nodeTypeId}</div>
      <Handle type="source" position={Position.Right} className="!bg-primary" />
    </div>
  )
}

const nodeTypes = { queryNode: QueryFlowNode }

let nodeSeq = 1

export function FlowCanvas() {
  const [registryNodes, setRegistryNodes] = useState<NodeTypeDefinition[]>([])
  const [nodes, setNodes, onNodesChange] = useNodesState<Node<FlowNodeData>>([])
  const [edges, setEdges, onEdgesChange] = useEdgesState<Edge<FlowEdgeData>>([])
  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null)
  const [selectedEdgeId, setSelectedEdgeId] = useState<string | null>(null)
  const [running, setRunning] = useState(false)
  const [runResult, setRunResult] = useState<GraphExecuteResponse | null>(null)

  useEffect(() => {
    fetchRegistry().then((registry) => {
      setRegistryNodes(registry.node_types.filter((node) => node.kind === 'query' && node.preset))
    })
  }, [])

  const groupedNodes = useMemo(() => {
    const groups = new Map<string, NodeTypeDefinition[]>()
    for (const node of registryNodes) {
      const list = groups.get(node.category) ?? []
      list.push(node)
      groups.set(node.category, list)
    }
    return groups
  }, [registryNodes])

  const selectedNode = nodes.find((node) => node.id === selectedNodeId)
  const selectedEdge = edges.find((edge) => edge.id === selectedEdgeId)
  const selectedNodeDef = registryNodes.find((node) => node.id === selectedNode?.data.nodeTypeId)

  const addNode = useCallback(
    (nodeType: NodeTypeDefinition) => {
      const id = `n${nodeSeq++}`
      const x = 120 + (nodes.length % 4) * 260
      const y = 80 + Math.floor(nodes.length / 4) * 140
      setNodes((current) => [
        ...current,
        {
          id,
          type: 'queryNode',
          position: { x, y },
          data: {
            nodeTypeId: nodeType.id,
            label: nodeType.label,
            category: nodeType.category,
            supportedFilters: nodeType.supported_filters,
            constInputs: {},
          },
        },
      ])
      setSelectedNodeId(id)
      setSelectedEdgeId(null)
    },
    [nodes.length, setNodes],
  )

  const onConnect = useCallback(
    (connection: Connection) => {
      const targetNode = nodes.find((node) => node.id === connection.target)
      const defaultTargetInput = targetNode?.data.supportedFilters[0] ?? 'project'
      setEdges((current) =>
        addEdge(
          {
            ...connection,
            data: {
              sourceField: '项目号',
              targetInput: defaultTargetInput,
            },
          },
          current,
        ),
      )
      setSelectedEdgeId(connection.target ?? null)
    },
    [nodes, setEdges],
  )

  const updateNodeInput = (key: string, value: string) => {
    if (!selectedNodeId) return
    setNodes((current) =>
      current.map((node) =>
        node.id === selectedNodeId
          ? {
              ...node,
              data: {
                ...node.data,
                constInputs: { ...node.data.constInputs, [key]: value },
              },
            }
          : node,
      ),
    )
  }

  const updateEdgeMapping = (field: 'sourceField' | 'targetInput', value: string) => {
    if (!selectedEdgeId) return
    setEdges((current) =>
      current.map((edge) =>
        edge.id === selectedEdgeId
          ? { ...edge, data: { ...(edge.data ?? { sourceField: '', targetInput: '' }), [field]: value } }
          : edge,
      ),
    )
  }

  const runGraph = async () => {
    if (nodes.length === 0) return
    setRunning(true)
    setRunResult(null)
    try {
      const response = await graphExecute(
        nodes.map((node) => ({
          id: node.id,
          type: node.data.nodeTypeId,
          inputs: Object.fromEntries(
            Object.entries(node.data.constInputs)
              .filter(([, value]) => value.trim() !== '')
              .map(([key, value]) => [key, { mode: 'const' as const, value }]),
          ),
        })),
        edges.map((edge) => ({
          source: edge.source,
          target: edge.target,
          source_field: edge.data?.sourceField ?? '',
          target_input: edge.data?.targetInput ?? '',
        })),
      )
      setRunResult(response)
    } catch (err) {
      alert(err instanceof Error ? err.message : String(err))
    } finally {
      setRunning(false)
    }
  }

  return (
    <div className="grid grid-cols-1 gap-4 xl:grid-cols-[240px_minmax(0,1fr)_280px]">
      <Card className="max-h-[calc(100vh-8rem)] overflow-hidden">
        <CardHeader>
          <CardTitle className="text-sm">节点面板</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3 overflow-y-auto px-3 pb-3">
          {[...groupedNodes.entries()].map(([category, items]) => (
            <div key={category} className="space-y-1.5">
              <div className="text-xs font-medium text-muted-foreground">{category}</div>
              {items.map((item) => (
                <button
                  key={item.id}
                  type="button"
                  onClick={() => addNode(item)}
                  className="flex w-full items-start gap-2 rounded-md border px-2 py-2 text-left hover:bg-accent/50"
                >
                  <PlusIcon className="mt-0.5 size-3.5 shrink-0" />
                  <span className="text-xs leading-tight">{item.label}</span>
                </button>
              ))}
            </div>
          ))}
        </CardContent>
      </Card>

      <div className="relative min-h-[calc(100vh-8rem)] overflow-hidden rounded-lg border bg-card">
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          nodeTypes={nodeTypes}
          onNodeClick={(_, node) => {
            setSelectedNodeId(node.id)
            setSelectedEdgeId(null)
          }}
          onEdgeClick={(_, edge) => {
            setSelectedEdgeId(edge.id)
            setSelectedNodeId(null)
          }}
          fitView
        >
          <Background gap={20} size={1} />
          <MiniMap zoomable pannable />
          <Controls />
        </ReactFlow>
        <div className="absolute right-3 top-3">
          <Button size="sm" onClick={runGraph} disabled={running || nodes.length === 0}>
            <PlayIcon className="mr-1 size-3.5" />
            {running ? '执行中...' : '执行节点图'}
          </Button>
        </div>
      </div>

      <Card className="max-h-[calc(100vh-8rem)] overflow-hidden">
        <CardHeader>
          <CardTitle className="text-sm">属性面板</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4 overflow-y-auto px-3 pb-3">
          {selectedNode && selectedNodeDef ? (
            <>
              <div>
                <div className="mb-1 flex items-center gap-2">
                  <Badge variant="secondary">{selectedNode.data.category}</Badge>
                </div>
                <div className="text-sm font-medium">{selectedNode.data.label}</div>
              </div>
              <div className="space-y-2">
                <div className="text-xs font-medium text-muted-foreground">常量筛选条件</div>
                {selectedNodeDef.supported_filters.map((key) => (
                  <div key={key} className="space-y-1">
                    <Label htmlFor={`input-${key}`}>{key}</Label>
                    <Input
                      id={`input-${key}`}
                      value={selectedNode.data.constInputs[key] ?? ''}
                      onChange={(e) => updateNodeInput(key, e.target.value)}
                      className="h-8 text-xs"
                    />
                  </div>
                ))}
              </div>
            </>
          ) : selectedEdge ? (
            <div className="space-y-3">
              <div className="text-xs text-muted-foreground">连线字段映射</div>
              <div className="space-y-1">
                <Label htmlFor="source-field">上游输出字段</Label>
                <Input
                  id="source-field"
                  value={selectedEdge.data?.sourceField ?? ''}
                  onChange={(e) => updateEdgeMapping('sourceField', e.target.value)}
                  placeholder="例: 项目号"
                  className="h-8 text-xs"
                />
              </div>
              <div className="space-y-1">
                <Label htmlFor="target-input">下游输入字段</Label>
                <Input
                  id="target-input"
                  value={selectedEdge.data?.targetInput ?? ''}
                  onChange={(e) => updateEdgeMapping('targetInput', e.target.value)}
                  placeholder="例: project"
                  className="h-8 text-xs"
                />
              </div>
            </div>
          ) : (
            <p className="text-xs text-muted-foreground">选择节点或连线以编辑属性。</p>
          )}

          {runResult && (
            <div className="space-y-2 border-t pt-3">
              <div className="text-xs font-medium text-muted-foreground">最近执行结果</div>
              {runResult.results.map((item) => (
                <div key={item.node_id} className="rounded-md border px-2 py-2 text-xs">
                  <div className="font-medium">{item.node_type_id}</div>
                  <div className="text-muted-foreground">
                    {item.error ? `错误: ${item.error}` : `${item.row_count} 行`}
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
