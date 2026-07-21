# Build the Vite frontend and sync web/dist -> server/static for Litestar.
# Usage: .\build-and-sync-static.ps1

$ErrorActionPreference = "Stop"

$Root = $PSScriptRoot
$WebDir = Join-Path $Root "web"
$DistDir = Join-Path $WebDir "dist"
$StaticDir = Join-Path (Join-Path $Root "server") "static"

if (-not (Test-Path $WebDir)) {
    throw "Web directory not found: $WebDir"
}

Write-Host "Building frontend in $WebDir ..."
Push-Location $WebDir
try {
    pnpm build
    if ($LASTEXITCODE -ne 0) {
        throw "pnpm build failed with exit code $LASTEXITCODE"
    }
} finally {
    Pop-Location
}

if (-not (Test-Path $DistDir)) {
    throw "Build output not found: $DistDir"
}

Write-Host "Syncing $DistDir -> $StaticDir ..."

if (Test-Path $StaticDir) {
    Get-ChildItem -Path $StaticDir -Force | Remove-Item -Recurse -Force
} else {
    New-Item -ItemType Directory -Path $StaticDir -Force | Out-Null
}

Copy-Item -Path (Join-Path $DistDir "*") -Destination $StaticDir -Recurse -Force

Write-Host "Done. Static files are ready for Litestar at $StaticDir"
