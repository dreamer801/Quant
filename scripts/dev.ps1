Param(
    [switch]$SkipFrontend
)

$ErrorActionPreference = "Stop"

$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Resolve-Path (Join-Path $scriptRoot "..")
Set-Location $repoRoot

Write-Host "Starting postgres via docker compose..."
docker compose up -d postgres | Out-Null

$databaseUrl = "postgresql+asyncpg://postgres:postgres@localhost:5432/quant_platform"

Write-Host "Launching backend dev server..."
$backendPath = Resolve-Path "backend"
Push-Location $backendPath
pip install -e .
Start-Process -FilePath "powershell" -ArgumentList "-NoExit","-Command","Set-Location `"$backendPath`"; $env:DATABASE_URL='$databaseUrl'; uvicorn app.main:app --reload"
Pop-Location

if (-not $SkipFrontend) {
    Write-Host "Launching frontend dev server..."
    $frontendPath = Resolve-Path "frontend"
    Push-Location $frontendPath
    npm install
    Start-Process -FilePath "powershell" -ArgumentList "-NoExit","-Command","Set-Location `"$frontendPath`"; npm run dev"
    Pop-Location
} else {
    Write-Host "SkipFrontend flag detected, not starting Next.js dev server."
}

Write-Host "Backend available at http://localhost:8000"
if (-not $SkipFrontend) {
    Write-Host "Frontend available at http://localhost:3000"
}
Write-Host "Use Ctrl+C in spawned PowerShell windows to stop services."
