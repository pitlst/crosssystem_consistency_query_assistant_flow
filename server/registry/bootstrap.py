from common import connect_source
from registry.models import (
    DataSourceDefinition,
    FilterSchemaEntry,
    NodeKind,
    NodePortDefinition,
    NodeTypeDefinition,
    PortDataType,
    RegistrySnapshot,
)
from sql import QUERY_REGISTRY

STANDARD_FILTER_PORTS: list[NodePortDefinition] = [
    NodePortDefinition(key="project", label="项目编码", data_type=PortDataType.STRING, role="filter"),
    NodePortDefinition(key="track_number", label="车号", data_type=PortDataType.POSITIVE_INT, role="filter"),
    NodePortDefinition(key="jch_num", label="节车号", data_type=PortDataType.ALNUM_CI, role="filter"),
    NodePortDefinition(key="process", label="工序编码", data_type=PortDataType.STRING, role="filter"),
    NodePortDefinition(key="material", label="物料编码", data_type=PortDataType.STRING, role="filter"),
    NodePortDefinition(key="order_code", label="生产订单编码", data_type=PortDataType.STRING, role="filter"),
]

FILTER_SCHEMA: dict[str, FilterSchemaEntry] = {
    "project": FilterSchemaEntry(label="项目编码", data_type=PortDataType.STRING),
    "track_number": FilterSchemaEntry(label="车号", data_type=PortDataType.POSITIVE_INT),
    "jch_num": FilterSchemaEntry(label="节车号", data_type=PortDataType.ALNUM_CI),
    "process": FilterSchemaEntry(label="工序编码", data_type=PortDataType.STRING),
    "material": FilterSchemaEntry(label="物料编码", data_type=PortDataType.STRING),
    "order_code": FilterSchemaEntry(label="生产订单编码", data_type=PortDataType.STRING),
}

CONNECT_SOURCE_TO_DATASOURCE: dict[connect_source, str] = {
    connect_source.EAS: "eas",
    connect_source.MES_CG: "cgmes",
    connect_source.MES_CT: "ctmes",
    connect_source.MES_JC: "jcmes",
    connect_source.MES_ZXJ: "zxjmes",
    connect_source.MES_TZ: "tzmes",
}

DATASOURCE_DEFINITIONS: list[DataSourceDefinition] = [
    DataSourceDefinition(id="eas", label="EAS", driver="oracle"),
    DataSourceDefinition(id="cgmes", label="城轨MES", driver="oracle"),
    DataSourceDefinition(id="ctmes", label="车体MES", driver="oracle"),
    DataSourceDefinition(id="jcmes", label="机车MES", driver="oracle"),
    DataSourceDefinition(id="zxjmes", label="转向架MES", driver="oracle"),
    DataSourceDefinition(id="tzmes", label="涂装MES", driver="oracle"),
    DataSourceDefinition(id="clickhouse_ref", label="ClickHouse参考库", driver="clickhouse"),
]

NODE_SUPPORTED_FILTERS: dict[str, list[str]] = {
    "eas_pbom": ["project", "track_number", "process", "material"],
    "eas_order": ["project", "track_number", "jch_num", "process", "material"],
    "eas_rooting": ["project", "track_number", "jch_num", "process", "material"],
    "eas_production_material": ["project", "track_number", "jch_num", "process", "material"],
    "eas_material_request": ["project", "track_number", "jch_num", "process", "material"],
    "eas_rework_order": ["project", "track_number", "jch_num", "process", "material"],
    "eas_order_exec_record": ["project", "track_number", "jch_num", "process", "material"],
    "eas_material_kitting": ["project", "track_number", "jch_num", "process", "material"],
    "eas_project_plan": ["project", "track_number", "jch_num", "material"],
    "cgmes_pbom": ["project", "track_number", "process", "material"],
    "cgmes_diagnose_order_bom": ["project", "track_number", "process", "material"],
    "cgmes_scheduling": ["project", "track_number", "jch_num", "process"],
    "cgmes_order_scheduling": ["project", "track_number", "jch_num", "process"],
    "cgmes_record": ["project", "track_number", "jch_num", "process", "material"],
    "cgmes_request": ["project", "track_number", "jch_num", "process", "material"],
    "cgmes_diagnose_pick": ["project", "track_number", "jch_num", "process", "material"],
    "cgmes_rework_order": ["project", "track_number", "jch_num", "process", "material"],
    "cgmes_rework_production_request": ["project", "track_number", "jch_num", "process", "material"],
}

PRESET_NODE_IDS = frozenset(NODE_SUPPORTED_FILTERS.keys())


def _category_for_node(node_id: str, label: str) -> str:
    if node_id.startswith("eas_"):
        return "EAS"
    if node_id.startswith("cgmes_"):
        return "城轨MES"
    if node_id.startswith("ctmes_"):
        return "车体MES"
    if node_id.startswith("jcmes_"):
        return "机车MES"
    if node_id.startswith("zxjmes_"):
        return "转向架MES"
    if node_id.startswith("tzmes_"):
        return "涂装MES"
    return label.split(" - ", 1)[0]


def build_query_node_definitions() -> list[NodeTypeDefinition]:
    definitions: list[NodeTypeDefinition] = []
    for node_id, (_builder, source, label) in QUERY_REGISTRY.items():
        supported = NODE_SUPPORTED_FILTERS.get(node_id, [p.key for p in STANDARD_FILTER_PORTS[:5]])
        definitions.append(
            NodeTypeDefinition(
                id=node_id,
                kind=NodeKind.QUERY,
                label=label,
                category=_category_for_node(node_id, label),
                datasource_id=CONNECT_SOURCE_TO_DATASOURCE[source],
                preset=node_id in PRESET_NODE_IDS,
                inputs=[port for port in STANDARD_FILTER_PORTS if port.key in supported or port.key == "order_code"],
                outputs=[],
                supported_filters=supported,
                enabled=True,
                source="builtin",
            )
        )
    return definitions


RESOLVER_NODE_DEFINITIONS: list[NodeTypeDefinition] = [
    NodeTypeDefinition(
        id="resolver_project_code",
        kind=NodeKind.RESOLVER,
        label="项目名称 → 项目号",
        category="参考库",
        datasource_id="clickhouse_ref",
        preset=True,
        inputs=[NodePortDefinition(key="project_name", label="项目名称", data_type=PortDataType.STRING, role="filter")],
        outputs=[
            NodePortDefinition(key="项目号", label="项目号", data_type=PortDataType.STRING, role="column"),
            NodePortDefinition(key="项目名称", label="项目名称", data_type=PortDataType.STRING, role="column"),
        ],
        supported_filters=["project_name"],
        enabled=True,
        source="builtin",
    ),
    NodeTypeDefinition(
        id="resolver_process_code",
        kind=NodeKind.RESOLVER,
        label="工序名称 → 工序编码",
        category="参考库",
        datasource_id="clickhouse_ref",
        preset=True,
        inputs=[NodePortDefinition(key="process_name", label="工序名称", data_type=PortDataType.STRING, role="filter")],
        outputs=[
            NodePortDefinition(key="工序编码", label="工序编码", data_type=PortDataType.STRING, role="column"),
            NodePortDefinition(key="工序名称", label="工序名称", data_type=PortDataType.STRING, role="column"),
        ],
        supported_filters=["process_name"],
        enabled=True,
        source="builtin",
    ),
    NodeTypeDefinition(
        id="resolver_material_code",
        kind=NodeKind.RESOLVER,
        label="物料名称 → 物料编码",
        category="参考库",
        datasource_id="clickhouse_ref",
        preset=True,
        inputs=[NodePortDefinition(key="material_name", label="物料名称", data_type=PortDataType.STRING, role="filter")],
        outputs=[
            NodePortDefinition(key="物料编码", label="物料编码", data_type=PortDataType.STRING, role="column"),
            NodePortDefinition(key="物料名称", label="物料名称", data_type=PortDataType.STRING, role="column"),
        ],
        supported_filters=["material_name"],
        enabled=True,
        source="builtin",
    ),
]


def build_registry_snapshot() -> RegistrySnapshot:
    return RegistrySnapshot(
        sources=DATASOURCE_DEFINITIONS,
        node_types=[*build_query_node_definitions(), *RESOLVER_NODE_DEFINITIONS],
        filter_schema=FILTER_SCHEMA,
    )
