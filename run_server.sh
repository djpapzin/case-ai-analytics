#!/bin/bash
# Activate conda environment and run FastAPI server
# Make sure this script is executable: chmod +x run_server.sh

# Source conda activation script
source ~/miniconda3/etc/profile.d/conda.sh

# Activate the environment
conda activate ai-automation

# Run the server with nohup to keep it running after terminal closes
nohup python -m uvicorn api:app --host 0.0.0.0 --port 5000 > server.log 2>&1 &

# Get process ID
PID=$!
echo "Server started on port 5000. Process ID: $PID"
echo "Server output is being logged to server.log"
echo "Access the API at http://154.0.164.254:5000/"
echo "To test the API, use: curl http://154.0.164.254:5000/"
echo "To stop the server, use: kill $PID" 