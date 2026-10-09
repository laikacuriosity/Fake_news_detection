$ErrorActionPreference = "Stop"

$env:PYTHONPATH = "C:\alethia\backend"

# Clean up any lingering processes on ports 8000 and 3000
$ports = 8000, 3000
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
Write-Host "Starting Aletheia Backend on port 8000..."
$BackendArgs = "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"
$BackendProcess = Start-Process -FilePath "C:\alethia\venv\Scripts\python.exe" -ArgumentList $BackendArgs -WorkingDirectory "C:\alethia\backend" -PassThru -NoNewWindow

# Start the Frontend
Write-Host "Starting Frontend on port 3000..."
$FrontendArgs = "-m", "http.server", "3000", "--directory", "C:\alethia\frontend"
$FrontendProcess = Start-Process -FilePath "C:\alethia\venv\Scripts\python.exe" -ArgumentList $FrontendArgs -PassThru -NoNewWindow

Write-Host ""
Write-Host "======================================================"
Write-Host "ALETHEIA CASE FILE is running!"
Write-Host "Frontend UI: http://localhost:3000"
Write-Host "Backend API: http://localhost:8000"
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
