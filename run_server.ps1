# PowerShell script to run the API server on port 5000
# Make sure to run this from the project root directory

# Activate conda environment
conda activate ai-automation

# Set environment variables
$env:PYTHONUNBUFFERED = "1"

# Kill any existing process on port 5000 (if needed)
$processToKill = Get-NetTCPConnection -LocalPort 5000 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess
if ($processToKill) {
    Write-Host "Killing existing process on port 5000 (PID: $processToKill)"
    Stop-Process -Id $processToKill -Force
}

# Start the server using PowerShell's background job feature (similar to nohup)
Write-Host "Starting API server on port 5000..."
$job = Start-Job -ScriptBlock {
    Set-Location $using:PWD
    # Use python directly with uvicorn to ensure port 5000
    python -c "import uvicorn; uvicorn.run('api:app', host='0.0.0.0', port=5000)"
}

Write-Host "API server is running in the background (Job ID: $($job.Id))"
Write-Host "You can access it at http://154.0.164.254:5000/"
Write-Host "To test: Invoke-RestMethod -Uri http://154.0.164.254:5000/"
Write-Host ""
Write-Host "To stop the server, run: Stop-Job -Id $($job.Id); Remove-Job -Id $($job.Id)" 