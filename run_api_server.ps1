# PowerShell script to run the API server
# Activate conda environment and run the API server on port 5000

Write-Host "Activating conda environment ai-automation..."

try {
    # Activate conda environment
    conda activate ai-automation

    # Set the environment variables
    $env:PYTHONUNBUFFERED = "1"

    # Run the API server with uvicorn and keep it running in the background
    # Using PowerShell Start-Process to run in background
    $processInfo = Start-Process -FilePath "python" -ArgumentList "-m uvicorn api:app --host 0.0.0.0 --port 5000" -NoNewWindow -PassThru

    if ($processInfo) {
        Write-Host "API server is running in the background on port 5000 with process ID: $($processInfo.Id)"
        Write-Host "You can access it at http://154.0.164.254:5000/"
        Write-Host "To test: curl http://154.0.164.254:5000/"
    } else {
        Write-Host "Failed to start the server. Please check if port 5000 is available."
    }
} catch {
    Write-Host "Error starting the server: $_"
} 