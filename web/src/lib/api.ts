export interface QueryOption {
  value: string
  label: string
}

export interface RegistrySnapshot {
  sources: Array<{
    id: string
    label: string
    driver: string
    enabled: boolean
    source: string
  }>
  node_types: NodeTypeDefinition[]
  filter_schema: Record<string, { label: string; data_type: string }>
}

export interface NodeTypeDefinition {
  id: string
  kind: 'query' | 'resolver'
  label: string
  category: string
  datasource_id: string
  preset: boolean
  inputs: Array<{ key: string; label: string; data_type: string; role: string }>
  outputs: Array<{ key: string; label: string; data_type: string; role: string }>
  supported_filters: string[]
  enabled: boolean
  source: string
}

export interface QueryRequest {
  project?: string | null
  track_number?: number | null
  jch_num?: string | null
  process?: string | null
  material?: string | null
  order_code?: string | null
}

export interface QueryResult {
  name: string
  data: Record<string, unknown>[]
  error: string | null
}

export interface NodeExecuteResponse {
  node_type_id: string
  columns: string[]
  rows: Record<string, unknown>[]
  row_count: number
  error: string | null
  duration_ms?: number | null
}

export interface BatchExecuteResponse {
  results: Array<{
    node_type_id: string
    columns: string[]
    rows: Record<string, unknown>[]
    row_count: number
    error: string | null
    duration_ms?: number | null
  }>
}

export interface ProjectCode {
  项目号: string
  项目名称: string
}

export interface ProcessCode {
  工序编码: string
  工序名称: string
}

export interface MaterialCode {
  物料编码: string
  物料名称: string
}

export interface GraphEdgeSpec {
  source: string
  target: string
  source_field: string
  target_input: string
}

export interface GraphNodeSpec {
  id: string
  type: string
  inputs: Record<string, { mode: 'const' | 'ref' | 'unset'; value?: unknown; node_id?: string; field?: string }>
}

export interface GraphExecuteResponse {
  results: Array<{
    node_id: string
    node_type_id: string
    columns: string[]
    rows: Record<string, unknown>[]
    row_count: number
    error: string | null
    duration_ms?: number | null
  }>
}

export async function fetchRegistry(): Promise<RegistrySnapshot> {
  const res = await fetch('/api/registry')
  if (!res.ok) throw new Error(`HTTP ${res.status}`)
  return res.json()
}

export async function fetchQueryOptions(): Promise<QueryOption[]> {
  const registry = await fetchRegistry()
  return registry.node_types
    .filter((node) => node.kind === 'query' && node.enabled)
    .map((node) => ({ value: node.id, label: node.label }))
}

export async function executeNode(
  nodeTypeId: string,
  inputs: Record<string, unknown>,
): Promise<NodeExecuteResponse> {
  const res = await fetch(`/api/nodes/${nodeTypeId}/execute`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ inputs }),
  })
  if (!res.ok) {
    const text = await res.text()
    throw new Error(`HTTP ${res.status}: ${text}`)
  }
  return res.json()
}

export async function fetchOne(queryName: string, params: QueryRequest): Promise<QueryResult> {
  const response = await executeNode(queryName, params as Record<string, unknown>)
  return {
    name: response.node_type_id,
    data: response.rows,
    error: response.error,
  }
}

export async function batchExecute(
  nodeTypeIds: string[],
  inputs: QueryRequest,
): Promise<QueryResult[]> {
  const res = await fetch('/api/batch/execute', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ node_type_ids: nodeTypeIds, inputs: paramsToInputs(inputs) }),
  })
  if (!res.ok) {
    const text = await res.text()
    throw new Error(`HTTP ${res.status}: ${text}`)
  }
  const json: BatchExecuteResponse = await res.json()
  return json.results.map((item) => ({
    name: item.node_type_id,
    data: item.rows,
    error: item.error,
  }))
}

function paramsToInputs(params: QueryRequest): Record<string, unknown> {
  const inputs: Record<string, unknown> = {}
  for (const [key, value] of Object.entries(params)) {
    if (value !== null && value !== undefined && value !== '') {
      inputs[key] = value
    }
  }
  return inputs
}

export async function fetchProjectCodes(projectName: string): Promise<ProjectCode[]> {
  if (!projectName.trim()) return []
  const res = await fetch(`/api/project_codes?project_name=${encodeURIComponent(projectName)}`)
  if (!res.ok) return []
  const json = await res.json()
  return json.projects ?? []
}

export async function fetchProcessCodes(processName: string): Promise<ProcessCode[]> {
  if (!processName.trim()) return []
  const res = await fetch(`/api/process_codes?process_name=${encodeURIComponent(processName)}`)
  if (!res.ok) return []
  const json = await res.json()
  return json.codes ?? []
}

export async function fetchMaterialCodes(materialName: string): Promise<MaterialCode[]> {
  if (!materialName.trim()) return []
  const res = await fetch(`/api/material_codes?material_name=${encodeURIComponent(materialName)}`)
  if (!res.ok) return []
  const json = await res.json()
  return json.materials ?? []
}

export async function graphExecute(
  nodes: GraphNodeSpec[],
  edges: GraphEdgeSpec[],
): Promise<GraphExecuteResponse> {
  const res = await fetch('/api/graph/execute', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ nodes, edges }),
  })
  if (!res.ok) {
    const text = await res.text()
    throw new Error(`HTTP ${res.status}: ${text}`)
  }
  return res.json()
}

export async function resolveProjectCodes(projectName: string): Promise<ProjectCode[]> {
  const response = await executeNode('resolver_project_code', { project_name: projectName })
  return response.rows as unknown as ProjectCode[]
}

export async function resolveProcessCodes(processName: string): Promise<ProcessCode[]> {
  const response = await executeNode('resolver_process_code', { process_name: processName })
  return response.rows as unknown as ProcessCode[]
}

export type QueryName = string
