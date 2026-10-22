$ErrorActionPreference = "Stop"

$ProjectRoot = $PSScriptRoot
$env:PYTHONPATH = Join-Path $ProjectRoot "backend"
$PythonPath = Join-Path $ProjectRoot "venv\Scripts\python.exe"

# Fallback to system python if venv python not found
if (!(Test-Path $PythonPath)) {
    $PythonPath = "python"
}

# Clean up any lingering processes on ports 8008 and 3000
$ports = 8008, 3000
foreach ($p in $ports) {
    $conns = Get-NetTCPConnection -LocalPort $p -ErrorAction SilentlyContinue
    if ($conns) {
        $pids = $conns | Select-Object -ExpandProperty OwningProcess -Unique
        foreach ($procId in $pids) {
            if ($procId -gt 4) {
                Write-Host "Releasing port $p (PID $procId)..."
                Stop-Process -Id $procId -Force -ErrorAction SilentlyContinue
            }
        }
    }
}

# Start the Backend with auto-reload
Write-Host "Starting SatyaScan Backend on port 8008..."
$BackendArgs = "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8008", "--reload"
$BackendDir = Join-Path $ProjectRoot "backend"
$BackendProcess = Start-Process -FilePath $PythonPath -ArgumentList $BackendArgs -WorkingDirectory $BackendDir -PassThru -NoNewWindow

# Start the Frontend
Write-Host "Starting SatyaScan Frontend on port 3000..."
$FrontendDir = Join-Path $ProjectRoot "frontend"
$FrontendArgs = "-m", "http.server", "3000", "--directory", $FrontendDir
$FrontendProcess = Start-Process -FilePath $PythonPath -ArgumentList $FrontendArgs -PassThru -NoNewWindow

Write-Host ""
Write-Host "======================================================"
Write-Host "SATYASCAN TRUTH INTELLIGENCE PLATFORM IS RUNNING!"
Write-Host "Frontend UI: http://localhost:3000"
Write-Host "Backend API: http://localhost:8008"
Write-Host "API Docs:    http://localhost:8008/docs"
Write-Host "Press Ctrl+C to stop the servers."
Write-Host "======================================================"

try {
    while ($true) {
        Start-Sleep -Seconds 1
    }
} finally {
    Write-Host "Stopping servers..."
    Stop-Process -Id $BackendProcess.Id -Force -ErrorAction SilentlyContinue
    Stop-Process -Id $FrontendProcess.Id -Force -ErrorAction SilentlyContinue
}
