param(
  [ValidateSet("migrate","routes","serve","code")]
  [string]$Cmd = "serve"
)

$BACKEND = "C:\users\admin\vms-monorepo\vms-monorepo\backend"
$PY      = Join-Path $BACKEND ".venv\Scripts\python.exe"

if (!(Test-Path $BACKEND)) { Write-Error "Backend folder not found: $BACKEND"; exit 1 }
if (!(Test-Path $PY))      { Write-Error "Python venv not found: $PY"; exit 1 }

# sanity check – make sure imports resolve to THIS backend
$check = & $PY -c "import sys, os, inspect; sys.path.insert(0, r'$BACKEND'); import app.main as m; p=inspect.getfile(m); print(p)"
if ($check -notlike "$BACKEND*") {
  Write-Error "app.main resolved to a DIFFERENT backend:`n$check"
  exit 1
}

switch ($Cmd) {
  "migrate" {
    & $PY "$BACKEND\migrate_all.py"
    if (Test-Path "$BACKEND\migrate_visitor_events.py") { & $PY "$BACKEND\migrate_visitor_events.py" }
    if (Test-Path "$BACKEND\add_created_by.py")        { & $PY "$BACKEND\add_created_by.py" }
    Write-Host "migrations done"
  }
  "routes" {
    & $PY -c "import sys; sys.path.insert(0, r'$BACKEND'); from app.main import app; print([(r.path, getattr(r,'methods',None)) for r in app.routes])"
  }
  "serve" {
    $args = @("-m","uvicorn","app.main:app","--reload","--reload-dir","app","--port","8000")
    Start-Process -FilePath $PY -ArgumentList $args -WorkingDirectory $BACKEND -NoNewWindow -Wait
  }
  "code" {
    Start-Process -FilePath "code" -ArgumentList $BACKEND
  }
}
