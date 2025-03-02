# PowerShell script to run the API server on port 5000
# Make sure to run this from the project root directory

# Activate conda environment and run FastAPI server
$condaPath = "C:\Users\lfana\miniconda3\Scripts\activate.ps1"
if (Test-Path $condaPath) {
    & $condaPath
    conda activate ai-automation
    
    # Run the FastAPI server with nohup equivalent in PowerShell
    # Using Start-Process to run in background
    $processInfo = Start-Process -FilePath python -ArgumentList "-m uvicorn api:app --host 0.0.0.0 --port 5000" -NoNewWindow -PassThru

    Write-Host "Server started on port 5000. Process ID: $($processInfo.Id)"
    Write-Host "Access the API at http://154.0.164.254:5000/"
    Write-Host "To test the API, use: curl http://154.0.164.254:5000/"
} else {
    Write-Host "Conda activation script not found at $condaPath"
    Write-Host "Please modify the script with the correct path to your conda activation script."
} 