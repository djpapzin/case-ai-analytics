# PowerShell script to run the API server with nohup-like functionality
# This ensures the process continues running even if the terminal is closed

# Activate conda environment
conda activate ai-automation

# Create a job that runs in the background
$job = Start-Job -ScriptBlock {
    # Set working directory to match the current directory
    Set-Location $using:PWD
    
    # Run uvicorn directly to ensure we're using port 5000
    python -c "import uvicorn; uvicorn.run('api:app', host='0.0.0.0', port=5000)"
}

Write-Host "Started API server in background (Job ID: $($job.Id))"
Write-Host "The server is running on port 5000"
Write-Host "You can access it at http://154.0.164.254:5000/"
Write-Host "To test: curl http://154.0.164.254:5000/"
Write-Host "To stop the server, run: Stop-Job -Id $($job.Id); Remove-Job -Id $($job.Id)" 