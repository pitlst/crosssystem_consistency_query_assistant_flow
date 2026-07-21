from __future__ import annotations

from collections import defaultdict, deque

from executors.query_executor import execute_query_node
from registry.models import (
    GraphExecuteRequest,
    GraphExecuteResponse,
    GraphNodeResult,
    InputBinding,
)


def _topological_order(node_ids: list[str], edges: list) -> list[str]:
    incoming_count: dict[str, int] = {node_id: 0 for node_id in node_ids}
    outgoing: dict[str, list[str]] = defaultdict(list)

    for edge in edges:
        if edge.source not in incoming_count or edge.target not in incoming_count:
            continue
        incoming_count[edge.target] += 1
        outgoing[edge.source].append(edge.target)

    queue = deque(node_id for node_id, count in incoming_count.items() if count == 0)
    ordered: list[str] = []

    while queue:
        current = queue.popleft()
        ordered.append(current)
        for target in outgoing[current]:
            incoming_count[target] -= 1
            if incoming_count[target] == 0:
                queue.append(target)

    if len(ordered) != len(node_ids):
        raise ValueError("Graph contains cycles or disconnected unknown nodes")

    return ordered


def _resolve_binding(binding: InputBinding, node_results: dict[str, GraphNodeResult]) -> object | None:
    if binding.mode == "const":
        return binding.value
    if binding.mode == "ref" and binding.node_id and binding.field:
        upstream = node_results.get(binding.node_id)
        if upstream and upstream.rows:
            return upstream.rows[0].get(binding.field)
    return None


async def execute_graph(request: GraphExecuteRequest) -> GraphExecuteResponse:
    node_map = {node.id: node for node in request.nodes}
    order = _topological_order(list(node_map.keys()), request.edges)
    incoming_edges: dict[str, list] = defaultdict(list)
    for edge in request.edges:
        incoming_edges[edge.target].append(edge)

    node_results: dict[str, GraphNodeResult] = {}

    for node_id in order:
        spec = node_map[node_id]
        resolved_inputs: dict[str, object] = {}

        for input_key, binding in spec.inputs.items():
            value = _resolve_binding(binding, node_results)
            if value is not None and value != "":
                resolved_inputs[input_key] = value

        for edge in incoming_edges[node_id]:
            upstream = node_results.get(edge.source)
            if upstream and upstream.rows:
                value = upstream.rows[0].get(edge.source_field)
                if value is not None and value != "":
                    resolved_inputs[edge.target_input] = value

        response = await execute_query_node(spec.type, resolved_inputs)
        node_results[node_id] = GraphNodeResult(
            node_id=node_id,
            node_type_id=response.node_type_id,
            columns=response.columns,
            rows=response.rows,
            row_count=response.row_count,
            error=response.error,
            duration_ms=response.duration_ms,
        )

    return GraphExecuteResponse(results=[node_results[node_id] for node_id in order])
