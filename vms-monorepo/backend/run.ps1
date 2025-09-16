param(
  [switch]$StartServer = $false,
  [switch]$ListRoutes = $false
)

# Canonical backend root = this script's folder
$ROOT = Split-Path -Parent $MyInvocation.MyCommand.Path
Write-Host "Backend root: $ROOT"

# Use venv's Python directly
$PY = Join-Path $ROOT ".venv\Scripts\python.exe"
if (-not (Test-Path $PY)) {
  Write-Host "ERROR: $PY not found.`nCreate venv first:"
  Write-Host "  python -m venv .venv"
  Write-Host "  .\.venv\Scripts\Activate.ps1"
  Write-Host "  pip install -r requirements.txt"
  exit 1
}

function Run-ScriptIfExists([string]$file) {
  $path = Join-Path $ROOT $file
  if (Test-Path $path) {
    Write-Host "==> python $file"
    & $PY $path
    if ($LASTEXITCODE -ne 0) { throw "Script failed: $file" }
  } else {
    Write-Host "skip: $file (not found)"
  }
}

# --- One-off migration/setup helpers (runs only if present)
Run-ScriptIfExists "migrate_all.py"
Run-ScriptIfExists "add_user_role.py"
Run-ScriptIfExists "migrate_visitor_events.py"
Run-ScriptIfExists "migrate_notifications.py"
Run-ScriptIfExists "add_created_by.py"

if ($ListRoutes) {
  & $PY -c "from app.main import app; print([(r.path, getattr(r,'methods',None)) for r in app.routes])"
}

if ($StartServer) {
  Write-Host "==> starting uvicorn (reload on ./app)"
  & $PY -m uvicorn app.main:app --reload --reload-dir app --port 8000
}
