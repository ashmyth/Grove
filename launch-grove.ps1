<# 
.SYNOPSIS
    Grove (GeoPrithvi-Agri) Desktop Launcher
    Starts the FastAPI backend and Electron frontend together
#>

param(
    [switch]$Hidden
)

$rootDir = "E:\Downloads\Grove"
$frontendDir = Join-Path $rootDir "frontend"
$pythonCmd = if (Test-Path "python.exe") { "python.exe" } else { "python3" }

function Start-Backend {
    Write-Host "[Grove] Starting FastAPI backend on http://127.0.0.1:8000..." -ForegroundColor Cyan
    
    $backendProcess = Start-Process $pythonCmd -ArgumentList "-m", "uvicorn", "backend.main:app", "--host", "127.0.0.1", "--port", "8000" `
        -WorkingDirectory $rootDir `
        -WindowStyle Hidden `
        -PassThru
    
    return $backendProcess
}

function Test-BackendReady {
    try {
        $response = Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/v1/health" -TimeoutSec 5 -ErrorAction Stop -UseBasicParsing
        return $response.StatusCode -eq 200
    }
    catch {
        return $false
    }
}

function Start-Electron {
    Write-Host "[Grove] Starting Electron frontend..." -ForegroundColor Cyan
    
    $env:NODE_ENV = "production"
    Start-Process "npx" -ArgumentList "electron", "." -WorkingDirectory $frontendDir -WindowStyle Normal
}

# Main execution
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  GROVE (GeoPrithvi-Agri) - Canal Command Advisory System" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green

# Check if backend is already running
if (Test-BackendReady) {
    Write-Host "[Grove] Backend already running!" -ForegroundColor Yellow
}
else {
    $backendProc = Start-Backend
    
    # Wait for backend to be ready (up to 60 seconds)
    Write-Host "[Grove] Waiting for backend to start..." -ForegroundColor Yellow
    $maxWait = 60
    $waited = 0
    while (-not (Test-BackendReady) -and $waited -lt $maxWait) {
        Start-Sleep -Seconds 2
        $waited += 2
        Write-Host "." -NoNewline -ForegroundColor Gray
    }
    Write-Host ""
    
    if (Test-BackendReady) {
        Write-Host "[Grove] Backend ready!" -ForegroundColor Green
    }
    else {
        Write-Host "[Grove] WARNING: Backend health check timeout, but continuing..." -ForegroundColor Yellow
        Write-Host "[Grove] The backend may still be initializing." -ForegroundColor Yellow
    }
}

# Start Electron
Start-Electron

Write-Host "[Grove] Application launched successfully!" -ForegroundColor Green