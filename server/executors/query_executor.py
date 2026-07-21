import time
from typing import Any

from common import engine_query_to_json, filter_data
from database import create_clickhouse_client, create_connection
from logger import logger
from registry.bootstrap import CONNECT_SOURCE_TO_DATASOURCE
from registry import get_node_definition, get_query_runtime
from registry.models import BatchExecuteResponse, BatchExecuteResult, NodeExecuteResponse, NodeKind

_DATASOURCE_TO_CONNECT_SOURCE = {v: k for k, v in CONNECT_SOURCE_TO_DATASOURCE.items()}


def _inputs_to_filter_data(inputs: dict[str, Any]) -> filter_data:
    track_number = inputs.get("track_number")
    if track_number == "" or track_number is None:
        track_number = None
    elif not isinstance(track_number, int):
        try:
            track_number = int(track_number)
        except (TypeError, ValueError):
            track_number = None

    return filter_data(
        project=_nullable_str(inputs.get("project")),
        track_number=track_number,
        jch_num=_nullable_str(inputs.get("jch_num")),
        process=_nullable_str(inputs.get("process")),
        material=_nullable_str(inputs.get("material")),
        order_code=_nullable_str(inputs.get("order_code")),
    )


def _nullable_str(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _columns_from_rows(rows: list[dict[str, Any]]) -> list[str]:
    if not rows:
        return []
    return list(rows[0].keys())


def _escape_like(value: str) -> str:
    return value.replace("\\", "\\\\").replace("'", "''")


async def execute_resolver(node_id: str, inputs: dict[str, Any]) -> NodeExecuteResponse:
    started = time.perf_counter()
    client = create_clickhouse_client()
    try:
        from common import clickhouse_query_to_json

        if node_id == "resolver_project_code":
            project_name = _escape_like(_nullable_str(inputs.get("project_name")) or "")
            sql = (
                "SELECT DISTINCT \"项目号\", \"项目名称\" FROM dwd.project_integration_reference_materials "
                f"WHERE \"项目名称\" LIKE '%{project_name}%' LIMIT 50"
            )
        elif node_id == "resolver_process_code":
            process_name = _escape_like(_nullable_str(inputs.get("process_name")) or "")
            sql = (
                "SELECT DISTINCT \"工序编码\", \"工序名称\" FROM dwd.process_integration_reference_materials "
                f"WHERE \"工序名称\" LIKE '%{process_name}%' LIMIT 50"
            )
        elif node_id == "resolver_material_code":
            material_name = _escape_like(_nullable_str(inputs.get("material_name")) or "")
            sql = (
                "SELECT DISTINCT \"物料编码\", \"物料名称\" FROM dwd.process_integration_reference_materials "
                f"WHERE \"物料名称\" LIKE '%{material_name}%' LIMIT 50"
            )
        else:
            rows = []
            error = f"Unknown resolver node: {node_id}"
            duration_ms = int((time.perf_counter() - started) * 1000)
            return NodeExecuteResponse(
                node_type_id=node_id,
                columns=_columns_from_rows(rows),
                rows=rows,
                row_count=len(rows),
                error=error,
                duration_ms=duration_ms,
            )

        result = await clickhouse_query_to_json(client, sql, node_id)
        rows = result["data"]
        error = result["error"]
        duration_ms = int((time.perf_counter() - started) * 1000)
        return NodeExecuteResponse(
            node_type_id=node_id,
            columns=_columns_from_rows(rows),
            rows=rows,
            row_count=len(rows),
            error=error,
            duration_ms=duration_ms,
        )
    finally:
        client.close()


async def execute_query_node(node_id: str, inputs: dict[str, Any]) -> NodeExecuteResponse:
    started = time.perf_counter()
    definition = get_node_definition(node_id)
    if definition is None:
        return NodeExecuteResponse(
            node_type_id=node_id,
            columns=[],
            rows=[],
            row_count=0,
            error=f"Unknown node type: {node_id}",
        )

    if definition.kind == NodeKind.RESOLVER:
        return await execute_resolver(node_id, inputs)

    runtime = get_query_runtime(node_id)
    if runtime is None:
        return NodeExecuteResponse(
            node_type_id=node_id,
            columns=[],
            rows=[],
            row_count=0,
            error=f"Query runtime not registered for: {node_id}",
        )

    filters = _inputs_to_filter_data(inputs)
    connect = _DATASOURCE_TO_CONNECT_SOURCE.get(runtime.datasource_id)
    if connect is None:
        return NodeExecuteResponse(
            node_type_id=node_id,
            columns=[],
            rows=[],
            row_count=0,
            error=f"Unknown datasource: {runtime.datasource_id}",
        )

    engine = create_connection(connect)
    try:
        sql = runtime.sql_builder(filters)
        logger.info(f"[{node_id}] executing query against {runtime.datasource_id}")
        result = await engine_query_to_json(engine, sql, node_id)
        rows = result["data"]
        duration_ms = int((time.perf_counter() - started) * 1000)
        return NodeExecuteResponse(
            node_type_id=node_id,
            columns=_columns_from_rows(rows),
            rows=rows,
            row_count=len(rows),
            error=result["error"],
            duration_ms=duration_ms,
        )
    finally:
        engine.dispose()


async def execute_batch(node_type_ids: list[str], inputs: dict[str, Any]) -> BatchExecuteResponse:
    import asyncio

    async def run_one(node_id: str) -> BatchExecuteResult:
        response = await execute_query_node(node_id, inputs)
        return BatchExecuteResult(
            node_type_id=response.node_type_id,
            columns=response.columns,
            rows=response.rows,
            row_count=response.row_count,
            error=response.error,
            duration_ms=response.duration_ms,
        )

    results = await asyncio.gather(*(run_one(node_id) for node_id in node_type_ids))
    return BatchExecuteResponse(results=list(results))
