# PowerShell script to run the API server
# Activate conda environment and run the API server on port 5000

# Activate conda environment
conda activate ai-automation

# Set the environment variables
$env:PYTHONUNBUFFERED = "1"

# Run the API server with nohup to keep it running in the background
# Using PowerShell Start-Process to run in background
Start-Process -FilePath "python" -ArgumentList "api.py" -NoNewWindow

Write-Host "API server is running in the background on port 5000"
Write-Host "You can access it at http://154.0.164.254:5000/"
Write-Host "To test: curl http://154.0.164.254:5000/" 