from collections.abc import Callable
from enum import StrEnum
from typing import Any, Literal

from pydantic import BaseModel, Field

from common import filter_data


class NodeKind(StrEnum):
    QUERY = "query"
    RESOLVER = "resolver"


class PortDataType(StrEnum):
    STRING = "string"
    POSITIVE_INT = "positive_int"
    ALNUM_CI = "alnum_ci"


class NodePortDefinition(BaseModel):
    key: str
    label: str
    data_type: PortDataType
    role: Literal["filter", "column"] = "filter"
    required: bool = False


class DataSourceDefinition(BaseModel):
    id: str
    label: str
    driver: Literal["oracle", "clickhouse"]
    enabled: bool = True
    source: Literal["builtin", "config", "runtime"] = "builtin"


class NodeTypeDefinition(BaseModel):
    id: str
    kind: NodeKind
    label: str
    category: str
    datasource_id: str
    preset: bool = False
    inputs: list[NodePortDefinition] = Field(default_factory=list)
    outputs: list[NodePortDefinition] = Field(default_factory=list)
    supported_filters: list[str] = Field(default_factory=list)
    enabled: bool = True
    source: Literal["builtin", "config", "runtime"] = "builtin"


class FilterSchemaEntry(BaseModel):
    label: str
    data_type: PortDataType


class RegistrySnapshot(BaseModel):
    sources: list[DataSourceDefinition]
    node_types: list[NodeTypeDefinition]
    filter_schema: dict[str, FilterSchemaEntry]


class NodeExecuteRequest(BaseModel):
    inputs: dict[str, Any] = Field(default_factory=dict)
    options: dict[str, Any] = Field(default_factory=dict)


class NodeExecuteResponse(BaseModel):
    node_type_id: str
    columns: list[str]
    rows: list[dict[str, Any]]
    row_count: int
    error: str | None = None
    duration_ms: int | None = None


class BatchExecuteRequest(BaseModel):
    node_type_ids: list[str]
    inputs: dict[str, Any] = Field(default_factory=dict)
    options: dict[str, Any] = Field(default_factory=dict)


class BatchExecuteResult(BaseModel):
    node_type_id: str
    columns: list[str]
    rows: list[dict[str, Any]]
    row_count: int
    error: str | None = None
    duration_ms: int | None = None


class BatchExecuteResponse(BaseModel):
    results: list[BatchExecuteResult]


class InputBinding(BaseModel):
    mode: Literal["const", "ref", "unset"] = "unset"
    value: Any | None = None
    node_id: str | None = None
    field: str | None = None


class GraphNodeSpec(BaseModel):
    id: str
    type: str
    inputs: dict[str, InputBinding] = Field(default_factory=dict)


class GraphEdgeSpec(BaseModel):
    source: str
    target: str
    source_field: str
    target_input: str


class GraphExecuteRequest(BaseModel):
    nodes: list[GraphNodeSpec]
    edges: list[GraphEdgeSpec] = Field(default_factory=list)
    options: dict[str, Any] = Field(default_factory=dict)


class GraphNodeResult(BaseModel):
    node_id: str
    node_type_id: str
    columns: list[str]
    rows: list[dict[str, Any]]
    row_count: int
    error: str | None = None
    duration_ms: int | None = None


class GraphExecuteResponse(BaseModel):
    results: list[GraphNodeResult]


class QueryNodeRuntime:
    """Internal runtime binding for a registered query node."""

    __slots__ = ("definition", "sql_builder", "datasource_id")

    def __init__(
        self,
        definition: NodeTypeDefinition,
        sql_builder: Callable[[filter_data], str],
        datasource_id: str,
    ) -> None:
        self.definition = definition
        self.sql_builder = sql_builder
        self.datasource_id = datasource_id
