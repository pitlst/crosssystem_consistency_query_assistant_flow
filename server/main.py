import mimetypes
from pathlib import Path

import uvicorn
from litestar import Litestar
from litestar.static_files.config import create_static_files_router


STATIC_DIR = Path(__file__).resolve().parent / "static"

mimetypes.add_type("application/javascript", ".js")

static_files = create_static_files_router(
    path="/",
    directories=[STATIC_DIR],
    name="static",
    html_mode=True,
    include_in_schema=False,
)

app = Litestar(route_handlers=[static_files])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=12372)
