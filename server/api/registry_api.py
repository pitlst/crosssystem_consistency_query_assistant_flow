from litestar import get, post
from litestar.exceptions import NotFoundException

from executors.query_executor import execute_batch, execute_query_node
from registry import get_node_definition, get_registry_snapshot
from registry.models import (
    BatchExecuteRequest,
    BatchExecuteResponse,
    NodeExecuteRequest,
    NodeExecuteResponse,
    RegistrySnapshot,
)


@get("/api/registry")
async def get_registry() -> RegistrySnapshot:
    return get_registry_snapshot()


@get("/api/registry/node-types/{node_type_id:str}")
async def get_node_type(node_type_id: str) -> dict:
    definition = get_node_definition(node_type_id)
    if definition is None:
        raise NotFoundException(detail=f"Unknown node type: {node_type_id}")
    return definition.model_dump()


@post("/api/nodes/{node_type_id:str}/execute")
async def execute_node(node_type_id: str, data: NodeExecuteRequest) -> NodeExecuteResponse:
    return await execute_query_node(node_type_id, data.inputs)


@post("/api/batch/execute")
async def batch_execute(data: BatchExecuteRequest) -> BatchExecuteResponse:
    return await execute_batch(data.node_type_ids, data.inputs)
