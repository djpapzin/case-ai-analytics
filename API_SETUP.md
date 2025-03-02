# API Server Setup & Usage

This document explains how to set up and run the Case AI Analytics API server on different platforms.

## Prerequisites

1. Conda environment (Miniconda or Anaconda)
2. Required Python packages installed (see requirements.txt)

## Setup Instructions

### Windows

1. Activate the conda environment:
   ```powershell
   conda activate ai-automation
   ```

2. Run the provided PowerShell script:
   ```powershell
   .\run_server.ps1
   ```

   The server will start on port 5000.

### Linux/macOS

1. Make the shell script executable:
   ```bash
   chmod +x run_server.sh
   ```

2. Run the script:
   ```bash
   ./run_server.sh
   ```

   The server will start on port 5000 with nohup, so it continues running even if you close the terminal.

## Manual Setup (All Platforms)

If you prefer to run the server manually:

1. Activate the conda environment:
   ```
   conda activate ai-automation
   ```

2. Start the server:
   ```
   python -m uvicorn api:app --host 0.0.0.0 --port 5000
   ```

## Testing the API

Once the server is running, you can test it using:

```
curl http://154.0.164.254:5000/
```

## Available Endpoints

- `GET /`: Root endpoint, returns a welcome message
- `POST /predict`: Predicts case resolution
- `GET /insights`: Provides insights on case data

For more details on request/response formats, see the API documentation in the README.md file.

## Troubleshooting

If the server fails to start:

1. Ensure port 5000 is not already in use
2. Verify that the conda environment has all required dependencies
3. Check the logs for error messages (server.log for Linux/macOS) 