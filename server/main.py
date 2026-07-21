import uvicorn
from litestar import Litestar
from litestar.config.cors import CORSConfig
from litestar.plugins.pydantic import PydanticPlugin
from litestar.static_files.config import create_static_files_router
from litestar.stores.memory import MemoryStore

from api.graph_api import graph_execute
from api.legacy_api import (
    list_queries_legacy,
    query_consistency_legacy,
    resolve_material_codes_by_name,
    resolve_process_codes_by_name,
    resolve_project_codes_by_name,
)
from api.registry_api import batch_execute, execute_node, get_node_type, get_registry

static_files = create_static_files_router(
    path="/",
    directories=["static"],
    name="static",
    html_mode=True,
    include_in_schema=False,
)

cors_config = CORSConfig(allow_origins=["*"], allow_methods=["GET", "POST"])

app = Litestar(
    route_handlers=[
        get_registry,
        get_node_type,
        execute_node,
        batch_execute,
        graph_execute,
        list_queries_legacy,
        query_consistency_legacy,
        resolve_project_codes_by_name,
        resolve_process_codes_by_name,
        static_files,
    ],
    plugins=[PydanticPlugin()],
    cors_config=cors_config,
    stores={"default": MemoryStore()},
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=12372)
