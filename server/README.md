## Frontend static server

This backend only serves the built frontend files from `server/static`. It does
not expose application APIs or connect to any database.

Build and sync the frontend from the repository root:

```powershell
.\build-and-sync-static.ps1
```

Start the server from `server`:

```powershell
uv run python main.py
```

The application listens on `http://127.0.0.1:12372` by default. The static
directory is generated and ignored by Git, so build the frontend before the
first start on a clean checkout.
