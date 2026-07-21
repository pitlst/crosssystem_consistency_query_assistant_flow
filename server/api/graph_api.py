from litestar import post
from litestar.exceptions import ClientException

from executors.graph_engine import execute_graph
from registry.models import GraphExecuteRequest, GraphExecuteResponse


@post("/api/graph/execute")
async def graph_execute(data: GraphExecuteRequest) -> GraphExecuteResponse:
    if not data.nodes:
        raise ClientException(detail="Graph must contain at least one node")
    try:
        return await execute_graph(data)
    except ValueError as exc:
        raise ClientException(detail=str(exc)) from exc
