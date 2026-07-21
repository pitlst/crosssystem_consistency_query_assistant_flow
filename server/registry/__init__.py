from collections.abc import Callable

from common import connect_source, filter_data
from registry.bootstrap import (
    CONNECT_SOURCE_TO_DATASOURCE,
    RESOLVER_NODE_DEFINITIONS,
    build_query_node_definitions,
    build_registry_snapshot,
)
from registry.models import (
    BatchExecuteResponse,
    BatchExecuteResult,
    NodeExecuteResponse,
    NodeKind,
    NodeTypeDefinition,
    QueryNodeRuntime,
    RegistrySnapshot,
)
from sql import QUERY_REGISTRY

_sources = {s.id: s for s in build_registry_snapshot().sources}
_node_definitions: dict[str, NodeTypeDefinition] = {
    node.id: node for node in [*build_query_node_definitions(), *RESOLVER_NODE_DEFINITIONS]
}
_query_runtimes: dict[str, QueryNodeRuntime] = {}


def _init_query_runtimes() -> None:
    if _query_runtimes:
        return
    for node_id, (sql_builder, source, _label) in QUERY_REGISTRY.items():
        definition = _node_definitions[node_id]
        _query_runtimes[node_id] = QueryNodeRuntime(
            definition=definition,
            sql_builder=sql_builder,
            datasource_id=CONNECT_SOURCE_TO_DATASOURCE[source],
        )


_init_query_runtimes()


def get_registry_snapshot() -> RegistrySnapshot:
    return build_registry_snapshot()


def get_node_definition(node_id: str) -> NodeTypeDefinition | None:
    return _node_definitions.get(node_id)


def list_node_definitions(*, kind: NodeKind | None = None, preset_only: bool = False) -> list[NodeTypeDefinition]:
    nodes = list(_node_definitions.values())
    if kind is not None:
        nodes = [node for node in nodes if node.kind == kind]
    if preset_only:
        nodes = [node for node in nodes if node.preset]
    return nodes


def register_query_node(
    node_id: str,
    label: str,
    category: str,
    datasource: connect_source,
    sql_builder: Callable[[filter_data], str],
    *,
    supported_filters: list[str] | None = None,
    preset: bool = False,
) -> None:
    """Runtime registration hook for additional query nodes."""
    datasource_id = CONNECT_SOURCE_TO_DATASOURCE[datasource]
    definition = NodeTypeDefinition(
        id=node_id,
        kind=NodeKind.QUERY,
        label=label,
        category=category,
        datasource_id=datasource_id,
        preset=preset,
        inputs=[],
        outputs=[],
        supported_filters=supported_filters or [],
        enabled=True,
        source="runtime",
    )
    _node_definitions[node_id] = definition
    _query_runtimes[node_id] = QueryNodeRuntime(
        definition=definition,
        sql_builder=sql_builder,
        datasource_id=datasource_id,
    )


def get_query_runtime(node_id: str) -> QueryNodeRuntime | None:
    return _query_runtimes.get(node_id)
