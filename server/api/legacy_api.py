from typing import Any

from litestar import get, post
from litestar.exceptions import NotFoundException

from common import query_request
from executors.query_executor import execute_query_node
from registry import get_registry_snapshot


@get("/api/queries", cache=86400)
async def list_queries_legacy() -> list[dict[str, str]]:
    registry = get_registry_snapshot()
    return [
        {"value": node.id, "label": node.label}
        for node in registry.node_types
        if node.kind == "query" and node.enabled
    ]


@post("/api/query/{query_name:str}")
async def query_consistency_legacy(query_name: str, data: query_request) -> dict[str, Any]:
    registry = get_registry_snapshot()
    known = {node.id for node in registry.node_types if node.kind == "query"}
    if query_name not in known:
        raise NotFoundException(detail=f"Unknown query: {query_name!r}")

    response = await execute_query_node(
        query_name,
        data.model_dump(exclude_none=True),
    )
    return {
        "data": {
            "name": response.node_type_id,
            "data": response.rows,
            "error": response.error,
        }
    }


@get("/api/project_codes", cache=86400)
async def resolve_project_codes_by_name(project_name: str) -> dict[str, Any]:
    response = await execute_query_node("resolver_project_code", {"project_name": project_name})
    if response.error:
        return {"projects": [], "error": response.error}
    return {"projects": response.rows}


@get("/api/process_codes", cache=86400)
async def resolve_process_codes_by_name(process_name: str) -> dict[str, Any]:
    response = await execute_query_node("resolver_process_code", {"process_name": process_name})
    if response.error:
        return {"codes": [], "error": response.error}
    return {"codes": response.rows}


@get("/api/material_codes", cache=86400)
async def resolve_material_codes_by_name(material_name: str) -> dict[str, Any]:
    response = await execute_query_node("resolver_material_code", {"material_name": material_name})
    if response.error:
        return {"materials": [], "error": response.error}
    return {"materials": response.rows}
