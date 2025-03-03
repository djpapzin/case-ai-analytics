# Advanced API Server Runner
param(
    [int]$Port = 5000,
    [switch]$Debug = $false,
    [string]$HostName = "0.0.0.0"
)

try {
    # Try to activate conda environment
    Write-Host "Activating conda environment ai-automation..."
    conda activate ai-automation
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Failed to activate conda environment. Trying alternative method..." -ForegroundColor Yellow
        # Alternative activation method
        & conda activate ai-automation
    }
    
    # Check if environment is activated
    $condaPrefix = $env:CONDA_PREFIX
    if (-not $condaPrefix) {
        Write-Host "Warning: Conda environment may not be properly activated." -ForegroundColor Yellow
    } else {
        Write-Host "Conda environment active: $condaPrefix" -ForegroundColor Green
    }
    
    # Run API server with more detailed options
    Write-Host "Starting API server on ${HostName}:${Port} (Debug: $Debug)..." -ForegroundColor Cyan
    
    if ($Debug) {
        # Run in debug mode with uvicorn directly
        python -m uvicorn src.api.api:app --host $HostName --port $Port --reload
    } else {
        # Run normal mode through our app entrypoint
        python app.py --run-server --port $Port
    }
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
    exit 1
} 