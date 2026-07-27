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

const MOCK_DELAY_MS = 80

const FILTER_INPUTS: NodeTypeDefinition['inputs'] = [
  { key: 'project', label: '项目编码', data_type: 'string', role: 'filter' },
  { key: 'track_number', label: '车号', data_type: 'positive_int', role: 'filter' },
  { key: 'jch_num', label: '节车号', data_type: 'alnum_ci', role: 'filter' },
  { key: 'process', label: '工序编码', data_type: 'string', role: 'filter' },
  { key: 'material', label: '物料编码', data_type: 'string', role: 'filter' },
  { key: 'order_code', label: '生产订单编码', data_type: 'string', role: 'filter' },
]

const MOCK_QUERY_DEFINITIONS: Array<{
  id: string
  label: string
  category: string
  datasourceId: string
  supportedFilters: string[]
}> = [
  { id: 'eas_pbom', label: 'EAS - PBOM/工序BOM信息', category: 'EAS', datasourceId: 'eas', supportedFilters: ['project', 'track_number', 'process', 'material'] },
  { id: 'eas_order', label: 'EAS - 生产订单信息', category: 'EAS', datasourceId: 'eas', supportedFilters: ['project', 'track_number', 'jch_num', 'process', 'material'] },
  { id: 'eas_rooting', label: 'EAS - 工艺路线信息', category: 'EAS', datasourceId: 'eas', supportedFilters: ['project', 'track_number', 'jch_num', 'process', 'material'] },
  { id: 'eas_production_material', label: 'EAS - 生产备料/备料计划时序簿信息', category: 'EAS', datasourceId: 'eas', supportedFilters: ['project', 'track_number', 'jch_num', 'process', 'material'] },
  { id: 'eas_material_request', label: 'EAS - 领料单信息', category: 'EAS', datasourceId: 'eas', supportedFilters: ['project', 'track_number', 'jch_num', 'process', 'material'] },
  { id: 'eas_rework_order', label: 'EAS - 返工订单/返工制造单信息', category: 'EAS', datasourceId: 'eas', supportedFilters: ['project', 'track_number', 'jch_num', 'process', 'material'] },
  { id: 'eas_order_exec_record', label: 'EAS - 生产订单变更执行记录', category: 'EAS', datasourceId: 'eas', supportedFilters: ['project', 'track_number', 'jch_num', 'process', 'material'] },
  { id: 'eas_material_kitting', label: 'EAS - 物料齐套性分析', category: 'EAS', datasourceId: 'eas', supportedFilters: ['project', 'track_number', 'jch_num', 'process', 'material'] },
  { id: 'eas_project_plan', label: 'EAS - 项目计划', category: 'EAS', datasourceId: 'eas', supportedFilters: ['project', 'track_number', 'jch_num', 'material'] },
  { id: 'cgmes_pbom', label: '城轨MES - 工序BOM信息', category: '城轨MES', datasourceId: 'cgmes', supportedFilters: ['project', 'track_number', 'process', 'material'] },
  { id: 'cgmes_diagnose_order_bom', label: '城轨MES - 订单BOM信息', category: '城轨MES', datasourceId: 'cgmes', supportedFilters: ['project', 'track_number', 'process', 'material'] },
  { id: 'cgmes_scheduling', label: '城轨MES - 模板排程信息', category: '城轨MES', datasourceId: 'cgmes', supportedFilters: ['project', 'track_number', 'jch_num', 'process'] },
  { id: 'cgmes_order_scheduling', label: '城轨MES - 订单排程结果', category: '城轨MES', datasourceId: 'cgmes', supportedFilters: ['project', 'track_number', 'jch_num', 'process'] },
  { id: 'cgmes_record', label: '城轨MES - 派工单信息', category: '城轨MES', datasourceId: 'cgmes', supportedFilters: ['project', 'track_number', 'jch_num', 'process', 'material'] },
  { id: 'cgmes_request', label: '城轨MES - 配送需求单', category: '城轨MES', datasourceId: 'cgmes', supportedFilters: ['project', 'track_number', 'jch_num', 'process', 'material'] },
  { id: 'cgmes_diagnose_pick', label: '城轨MES - 领料单信息', category: '城轨MES', datasourceId: 'cgmes', supportedFilters: ['project', 'track_number', 'jch_num', 'process', 'material'] },
  { id: 'cgmes_rework_order', label: '城轨MES - 返工订单信息', category: '城轨MES', datasourceId: 'cgmes', supportedFilters: ['project', 'track_number', 'jch_num', 'process', 'material'] },
  { id: 'cgmes_rework_production_request', label: '城轨MES - 返工制造单信息', category: '城轨MES', datasourceId: 'cgmes', supportedFilters: ['project', 'track_number', 'jch_num', 'process', 'material'] },
  { id: 'ctmes_request', label: '车体MES - 派工单信息', category: '车体MES', datasourceId: 'ctmes', supportedFilters: ['project', 'track_number', 'jch_num', 'process', 'material'] },
  { id: 'jcmes_request', label: '机车MES - 派工单信息', category: '机车MES', datasourceId: 'jcmes', supportedFilters: ['project', 'track_number', 'jch_num', 'process', 'material'] },
  { id: 'zxjmes_request', label: '转向架MES - 派工单信息', category: '转向架MES', datasourceId: 'zxjmes', supportedFilters: ['project', 'track_number', 'jch_num', 'process', 'material'] },
  { id: 'tzmes_request', label: '涂装MES - 派工单信息', category: '涂装MES', datasourceId: 'tzmes', supportedFilters: ['project', 'track_number', 'jch_num', 'process', 'material'] },
]

const MOCK_QUERY_NODES: NodeTypeDefinition[] = MOCK_QUERY_DEFINITIONS.map((definition) => ({
  id: definition.id,
  kind: 'query',
  label: definition.label,
  category: definition.category,
  datasource_id: definition.datasourceId,
  preset: definition.id.startsWith('eas_') || definition.id.startsWith('cgmes_'),
  inputs: FILTER_INPUTS.filter((input) => definition.supportedFilters.includes(input.key) || input.key === 'order_code'),
  outputs: [
    { key: '项目号', label: '项目号', data_type: 'string', role: 'column' },
    { key: '物料编码', label: '物料编码', data_type: 'string', role: 'column' },
    { key: '状态', label: '状态', data_type: 'string', role: 'column' },
  ],
  supported_filters: definition.supportedFilters,
  enabled: true,
  source: 'mock',
}))

const MOCK_RESOLVER_NODES: NodeTypeDefinition[] = [
  {
    id: 'resolver_project_code',
    kind: 'resolver',
    label: '项目名称 → 项目号',
    category: '参考库',
    datasource_id: 'mock-reference',
    preset: true,
    inputs: [{ key: 'project_name', label: '项目名称', data_type: 'string', role: 'filter' }],
    outputs: [
      { key: '项目号', label: '项目号', data_type: 'string', role: 'column' },
      { key: '项目名称', label: '项目名称', data_type: 'string', role: 'column' },
    ],
    supported_filters: ['project_name'],
    enabled: true,
    source: 'mock',
  },
  {
    id: 'resolver_process_code',
    kind: 'resolver',
    label: '工序名称 → 工序编码',
    category: '参考库',
    datasource_id: 'mock-reference',
    preset: true,
    inputs: [{ key: 'process_name', label: '工序名称', data_type: 'string', role: 'filter' }],
    outputs: [
      { key: '工序编码', label: '工序编码', data_type: 'string', role: 'column' },
      { key: '工序名称', label: '工序名称', data_type: 'string', role: 'column' },
    ],
    supported_filters: ['process_name'],
    enabled: true,
    source: 'mock',
  },
  {
    id: 'resolver_material_code',
    kind: 'resolver',
    label: '物料名称 → 物料编码',
    category: '参考库',
    datasource_id: 'mock-reference',
    preset: true,
    inputs: [{ key: 'material_name', label: '物料名称', data_type: 'string', role: 'filter' }],
    outputs: [
      { key: '物料编码', label: '物料编码', data_type: 'string', role: 'column' },
      { key: '物料名称', label: '物料名称', data_type: 'string', role: 'column' },
    ],
    supported_filters: ['material_name'],
    enabled: true,
    source: 'mock',
  },
]

const MOCK_PROJECT_CODES: ProjectCode[] = [
  { 项目号: 'P2026-001', 项目名称: '轨道交通A线增购项目' },
  { 项目号: 'P2026-002', 项目名称: '市域列车B线项目' },
  { 项目号: 'P2026-003', 项目名称: '地铁C线检修项目' },
  { 项目号: 'P2026-004', 项目名称: '城际列车D线改造项目' },
]

const MOCK_PROCESS_CODES: ProcessCode[] = [
  { 工序编码: 'GX-010', 工序名称: '车体组装' },
  { 工序编码: 'GX-020', 工序名称: '车顶总成安装' },
  { 工序编码: 'GX-030', 工序名称: '内装安装' },
  { 工序编码: 'GX-040', 工序名称: '电气接线' },
  { 工序编码: 'GX-050', 工序名称: '出厂检验' },
]

const MOCK_MATERIAL_CODES: MaterialCode[] = [
  { 物料编码: 'MAT-10001', 物料名称: '侧墙总成' },
  { 物料编码: 'MAT-10002', 物料名称: '车顶总成' },
  { 物料编码: 'MAT-20001', 物料名称: '客室座椅' },
  { 物料编码: 'MAT-30001', 物料名称: '线束组件' },
  { 物料编码: 'MAT-40001', 物料名称: '制动控制模块' },
]

type MockBaseRow = {
  项目号: string
  项目名称: string
  车号: number
  节车号: string
  工序编码: string
  工序名称: string
  物料编码: string
  物料名称: string
  生产订单编码: string
  计划数量: number
  实际数量: number
  单位: string
  计划日期: string
}

const MOCK_BASE_ROWS: MockBaseRow[] = [
  {
    项目号: 'P2026-001',
    项目名称: '轨道交通A线增购项目',
    车号: 1,
    节车号: 'A01',
    工序编码: 'GX-010',
    工序名称: '车体组装',
    物料编码: 'MAT-10001',
    物料名称: '侧墙总成',
    生产订单编码: 'MO-202607-001',
    计划数量: 12,
    实际数量: 8,
    单位: '件',
    计划日期: '2026-07-25',
  },
  {
    项目号: 'P2026-001',
    项目名称: '轨道交通A线增购项目',
    车号: 2,
    节车号: 'A02',
    工序编码: 'GX-020',
    工序名称: '车顶总成安装',
    物料编码: 'MAT-10002',
    物料名称: '车顶总成',
    生产订单编码: 'MO-202607-002',
    计划数量: 12,
    实际数量: 12,
    单位: '件',
    计划日期: '2026-07-24',
  },
  {
    项目号: 'P2026-002',
    项目名称: '市域列车B线项目',
    车号: 1,
    节车号: 'B01',
    工序编码: 'GX-030',
    工序名称: '内装安装',
    物料编码: 'MAT-20001',
    物料名称: '客室座椅',
    生产订单编码: 'MO-202607-101',
    计划数量: 24,
    实际数量: 20,
    单位: '件',
    计划日期: '2026-07-29',
  },
  {
    项目号: 'P2026-003',
    项目名称: '地铁C线检修项目',
    车号: 3,
    节车号: 'C03',
    工序编码: 'GX-040',
    工序名称: '电气接线',
    物料编码: 'MAT-30001',
    物料名称: '线束组件',
    生产订单编码: 'MO-202607-201',
    计划数量: 18,
    实际数量: 6,
    单位: '套',
    计划日期: '2026-08-02',
  },
  {
    项目号: 'P2026-004',
    项目名称: '城际列车D线改造项目',
    车号: 4,
    节车号: 'D04',
    工序编码: 'GX-050',
    工序名称: '出厂检验',
    物料编码: 'MAT-40001',
    物料名称: '制动控制模块',
    生产订单编码: 'MO-202607-301',
    计划数量: 8,
    实际数量: 8,
    单位: '套',
    计划日期: '2026-08-06',
  },
]

const MOCK_REGISTRY: RegistrySnapshot = {
  sources: [
    { id: 'eas', label: 'EAS', driver: 'mock', enabled: true, source: 'mock' },
    { id: 'cgmes', label: '城轨MES', driver: 'mock', enabled: true, source: 'mock' },
    { id: 'ctmes', label: '车体MES', driver: 'mock', enabled: true, source: 'mock' },
    { id: 'jcmes', label: '机车MES', driver: 'mock', enabled: true, source: 'mock' },
    { id: 'zxjmes', label: '转向架MES', driver: 'mock', enabled: true, source: 'mock' },
    { id: 'tzmes', label: '涂装MES', driver: 'mock', enabled: true, source: 'mock' },
    { id: 'mock-reference', label: '参考库', driver: 'mock', enabled: true, source: 'mock' },
  ],
  node_types: [...MOCK_QUERY_NODES, ...MOCK_RESOLVER_NODES],
  filter_schema: Object.fromEntries(
    FILTER_INPUTS.map((input) => [input.key, { label: input.label, data_type: input.data_type }]),
  ),
}

const MOCK_NODE_BY_ID = new Map(MOCK_REGISTRY.node_types.map((node) => [node.id, node]))
const MOCK_RESULT_COLUMNS = [
  '项目号',
  '项目名称',
  '车号',
  '节车号',
  '工序编码',
  '工序名称',
  '物料编码',
  '物料名称',
  '生产订单编码',
  '单据编码',
  '数据来源',
  '业务类型',
  '计划数量',
  '实际数量',
  '单位',
  '状态',
  '计划日期',
  '更新时间',
]

function respond<T>(value: T, delay = MOCK_DELAY_MS): Promise<T> {
  return new Promise((resolve) => setTimeout(() => resolve(value), delay))
}

function normalize(value: unknown): string {
  return String(value ?? '').trim().toLocaleLowerCase('zh-CN')
}

function matches(value: unknown, query: unknown): boolean {
  const normalizedQuery = normalize(query)
  return normalizedQuery === '' || normalize(value).includes(normalizedQuery)
}

function paramsToInputs(params: QueryRequest): Record<string, unknown> {
  const inputs: Record<string, unknown> = {}
  for (const [key, value] of Object.entries(params)) {
    if (value !== null && value !== undefined && value !== '') inputs[key] = value
  }
  return inputs
}

function cloneRegistry(): RegistrySnapshot {
  return {
    sources: MOCK_REGISTRY.sources.map((source) => ({ ...source })),
    node_types: MOCK_REGISTRY.node_types.map((node) => ({
      ...node,
      inputs: node.inputs.map((input) => ({ ...input })),
      outputs: node.outputs.map((output) => ({ ...output })),
      supported_filters: [...node.supported_filters],
    })),
    filter_schema: Object.fromEntries(
      Object.entries(MOCK_REGISTRY.filter_schema).map(([key, value]) => [key, { ...value }]),
    ),
  }
}

function filteredBaseRows(inputs: Record<string, unknown>): MockBaseRow[] {
  const filters: Array<[keyof QueryRequest, keyof MockBaseRow]> = [
    ['project', '项目号'],
    ['track_number', '车号'],
    ['jch_num', '节车号'],
    ['process', '工序编码'],
    ['material', '物料编码'],
    ['order_code', '生产订单编码'],
  ]
  return MOCK_BASE_ROWS.filter((row) =>
    filters.every(([inputKey, rowKey]) => matches(row[rowKey], inputs[inputKey])),
  )
}

function createQueryRows(nodeTypeId: string, inputs: Record<string, unknown>): Record<string, unknown>[] {
  const node = MOCK_NODE_BY_ID.get(nodeTypeId)
  if (!node || node.kind !== 'query') return []

  return filteredBaseRows(inputs).map((row, index) => ({
    ...row,
    单据编码: `${nodeTypeId.toUpperCase()}-${String(index + 1).padStart(3, '0')}`,
    数据来源: node.category,
    业务类型: node.label.replace(`${node.category} - `, ''),
    状态: row.实际数量 >= row.计划数量 ? '已完成' : row.实际数量 === 0 ? '未开始' : '进行中',
    更新时间: '2026-07-23 10:30:00',
  }))
}

function createResolverRows(nodeTypeId: string, inputs: Record<string, unknown>): Record<string, unknown>[] {
  if (nodeTypeId === 'resolver_project_code') {
    return MOCK_PROJECT_CODES.filter((item) => matches(item.项目号, inputs.project_name) || matches(item.项目名称, inputs.project_name)).map((item) => ({ ...item }))
  }
  if (nodeTypeId === 'resolver_process_code') {
    return MOCK_PROCESS_CODES.filter((item) => matches(item.工序编码, inputs.process_name) || matches(item.工序名称, inputs.process_name)).map((item) => ({ ...item }))
  }
  if (nodeTypeId === 'resolver_material_code') {
    return MOCK_MATERIAL_CODES.filter((item) => matches(item.物料编码, inputs.material_name) || matches(item.物料名称, inputs.material_name)).map((item) => ({ ...item }))
  }
  return []
}

function createNodeResponse(nodeTypeId: string, inputs: Record<string, unknown>): NodeExecuteResponse {
  const node = MOCK_NODE_BY_ID.get(nodeTypeId)
  if (!node) {
    return { node_type_id: nodeTypeId, columns: [], rows: [], row_count: 0, error: `未找到测试节点: ${nodeTypeId}` }
  }

  const rows = node.kind === 'resolver' ? createResolverRows(nodeTypeId, inputs) : createQueryRows(nodeTypeId, inputs)
  return {
    node_type_id: nodeTypeId,
    columns: node.kind === 'resolver' ? Object.keys(rows[0] ?? {}) : MOCK_RESULT_COLUMNS,
    rows,
    row_count: rows.length,
    error: null,
    duration_ms: 18,
  }
}

export async function fetchRegistry(): Promise<RegistrySnapshot> {
  return respond(cloneRegistry())
}

export async function fetchQueryOptions(): Promise<QueryOption[]> {
  return respond(
    MOCK_QUERY_NODES.filter((node) => node.enabled).map((node) => ({ value: node.id, label: node.label })),
  )
}

export async function executeNode(
  nodeTypeId: string,
  inputs: Record<string, unknown>,
): Promise<NodeExecuteResponse> {
  return respond(createNodeResponse(nodeTypeId, inputs))
}

export async function fetchOne(queryName: string, params: QueryRequest): Promise<QueryResult> {
  const response = await executeNode(queryName, paramsToInputs(params))
  return { name: response.node_type_id, data: response.rows, error: response.error }
}

export async function batchExecute(
  nodeTypeIds: string[],
  inputs: QueryRequest,
): Promise<QueryResult[]> {
  const normalizedInputs = paramsToInputs(inputs)
  const results: BatchExecuteResponse['results'] = nodeTypeIds.map((nodeTypeId) => {
    const response = createNodeResponse(nodeTypeId, normalizedInputs)
    return {
      node_type_id: response.node_type_id,
      columns: response.columns,
      rows: response.rows,
      row_count: response.row_count,
      error: response.error,
      duration_ms: response.duration_ms,
    }
  })
  return respond(results.map((item) => ({ name: item.node_type_id, data: item.rows, error: item.error })), 180)
}

export async function fetchProjectCodes(projectName: string): Promise<ProjectCode[]> {
  if (!projectName.trim()) return []
  return respond(
    MOCK_PROJECT_CODES.filter((item) => matches(item.项目号, projectName) || matches(item.项目名称, projectName)).map((item) => ({ ...item })),
  )
}

export async function fetchProcessCodes(processName: string): Promise<ProcessCode[]> {
  if (!processName.trim()) return []
  return respond(
    MOCK_PROCESS_CODES.filter((item) => matches(item.工序编码, processName) || matches(item.工序名称, processName)).map((item) => ({ ...item })),
  )
}

export async function fetchMaterialCodes(materialName: string): Promise<MaterialCode[]> {
  if (!materialName.trim()) return []
  return respond(
    MOCK_MATERIAL_CODES.filter((item) => matches(item.物料编码, materialName) || matches(item.物料名称, materialName)).map((item) => ({ ...item })),
  )
}

export async function graphExecute(
  nodes: GraphNodeSpec[],
  edges: GraphEdgeSpec[],
): Promise<GraphExecuteResponse> {
  const rowsByNode = new Map<string, Record<string, unknown>[]>()
  const results: GraphExecuteResponse['results'] = []

  for (const [index, graphNode] of nodes.entries()) {
    const inputs: Record<string, unknown> = {}
    for (const [key, input] of Object.entries(graphNode.inputs)) {
      if (input.mode === 'const') inputs[key] = input.value
    }
    for (const edge of edges.filter((item) => item.target === graphNode.id)) {
      const sourceRow = rowsByNode.get(edge.source)?.[0]
      if (sourceRow && sourceRow[edge.source_field] !== undefined) inputs[edge.target_input] = sourceRow[edge.source_field]
    }

    const response = createNodeResponse(graphNode.type, inputs)
    rowsByNode.set(graphNode.id, response.rows)
    results.push({
      node_id: graphNode.id,
      node_type_id: response.node_type_id,
      columns: response.columns,
      rows: response.rows,
      row_count: response.row_count,
      error: response.error,
      duration_ms: 18 + index * 7,
    })
  }

  return respond({ results }, 180)
}

export async function resolveProjectCodes(projectName: string): Promise<ProjectCode[]> {
  return fetchProjectCodes(projectName)
}

export async function resolveProcessCodes(processName: string): Promise<ProcessCode[]> {
  return fetchProcessCodes(processName)
}

export type QueryName = string
