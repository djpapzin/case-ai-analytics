# API Server Setup & Usage

This document explains how to set up and run the Case AI Analytics API server on different platforms.

## Prerequisites

1. Conda environment (Miniconda or Anaconda)
2. Required Python packages installed (see config/requirements.txt)
3. Python 3.11 or higher

## Setup Instructions

### Windows

1. Activate the conda environment:
   ```powershell
   conda activate ai-automation
   ```

2. Run the provided PowerShell script:
   ```powershell
   # Standard mode
   .\scripts\run_server.ps1

   # Debug mode
   .\scripts\run_api_server.ps1 -Debug
   ```

   The server will start on port 5000 by default.

### Linux/macOS

1. Make the shell script executable:
   ```bash
   chmod +x scripts/run_server.sh
   ```

2. Run the script:
   ```bash
   ./scripts/run_server.sh
   ```

   The server will start on port 5000 with nohup, so it continues running even if you close the terminal.

## Manual Setup (All Platforms)

If you prefer to run the server manually:

1. Activate the conda environment:
   ```bash
   conda activate ai-automation
   ```

2. Start the server:
   ```bash
   # Standard mode
   python app.py --run-server --port 5000

   # Debug mode
   python app.py --debug --run-server --port 5000
   ```

## Environment Variables

The following environment variables can be used to configure the server:

- `PORT`: Server port (default: 5000)
- `DEBUG`: Enable debug mode (true/false)
- `HOST`: Server host (default: 0.0.0.0)

## Testing the API

Once the server is running, you can test it using:

```bash
# Test root endpoint
curl http://localhost:5000/

# Test prediction endpoint
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"case_type": "Family Law", "complexity": "Medium", "client_age": 35, "client_income_level": "Medium", "days_open": 30, "escalated": false}'

# Test insights endpoint
curl -X POST http://localhost:5000/insights \
  -H "Content-Type: application/json" \
  -d '{"insight_type": "common_case_types"}'
```

## Available Endpoints

- `GET /`: Root endpoint, returns a welcome message and API status
- `POST /predict`: Predicts case resolution
- `POST /insights`: Provides insights on case data
- `GET /model-info`: Returns information about the trained model

For detailed request/response formats, see the API documentation in the README.md file.

## Error Handling

The API returns structured error responses in the following format:

```json
{
    "error": "Error type",
    "details": "Detailed error message",
    "timestamp": "2024-03-14T12:00:00Z"
}
```

Common error types:
- Feature validation errors
- Model loading errors
- Invalid input format
- Missing required fields

## Logging

Logs are stored in the following files:
- `logs/server.log`: Server operations
- `logs/model.log`: Model predictions
- `logs/api.log`: API requests/responses

Enable debug logging by starting the server in debug mode:
```bash
python app.py --debug
```

## Troubleshooting

If the server fails to start:

1. Check port availability:
   ```bash
   # Windows
   netstat -ano | findstr :5000
   
   # Linux/macOS
   lsof -i :5000
   ```

2. Verify conda environment:
   ```bash
   conda list
   ```

3. Common issues:
   - Port already in use
   - Missing dependencies
   - Invalid feature names in prediction requests
   - Incorrect data types in request payload

For more detailed troubleshooting, check the logs or enable debug mode. 