# PowerShell script to run the API server on port 5000
# Make sure to run this from the project root directory

# Run API Server with Conda Activation
param(
    [int]$Port = 5000
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
    
    # Run API server
    Write-Host "Starting API server on port $Port..." -ForegroundColor Cyan
    python app.py --run-server --port $Port
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
    exit 1
} 