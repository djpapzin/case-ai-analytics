# PowerShell script to run the API server on port 5000
# Make sure to run this from the project root directory

# Since conda is available as an alias in this environment, we can use it directly
# Activate conda environment 
Write-Host "Activating conda environment ai-automation..."

# Run the FastAPI server with nohup equivalent in PowerShell
# Using Start-Process to run in background
try {
    # Activate the conda environment
    conda activate ai-automation
    
    # Run the FastAPI server
    $processInfo = Start-Process -FilePath python -ArgumentList "-m uvicorn api:app --host 0.0.0.0 --port 5000" -NoNewWindow -PassThru

    if ($processInfo) {
        Write-Host "Server started on port 5000. Process ID: $($processInfo.Id)"
        Write-Host "Access the API at http://154.0.164.254:5000/"
        Write-Host "To test the API, use: curl http://154.0.164.254:5000/"
    } else {
        Write-Host "Failed to start the server. Please check if port 5000 is available."
    }
} catch {
    Write-Host "Error starting the server: $_"
} 