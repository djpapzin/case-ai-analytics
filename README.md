# Case AI Analytics

ML-powered system for predicting case outcomes and extracting insights from case management data. Uses Random Forest for resolution prediction and provides analysis on case types, resolution factors, and assignee performance. Includes FastAPI server for API access.

## Project Overview

This project consists of two main parts:
1. **Machine Learning Model**: Predicts case outcomes based on case management system data.
2. **AI Agent for Case Insights**: Provides actionable insights from the case management data.

## Project Structure

The project is organized into a modular structure:

```
case-ai-analytics/
├── app.py                  # Main application entry point
├── config/                 # Configuration files
│   ├── feature_mapping.json  # Feature mapping for ML model
│   └── requirements.txt    # Python dependencies
├── docs/                   # Documentation
│   ├── API_SETUP.md        # API setup instructions
│   ├── DEVELOPER_NOTES.md  # Technical notes for developers
│   └── README.md           # Detailed project documentation
├── scripts/                # Scripts for running the application
│   ├── run_api_server.ps1  # PowerShell script for running API server
│   ├── run_nohup.ps1       # PowerShell nohup equivalent
│   ├── run_server.ps1      # PowerShell script for running server
│   └── run_server.sh       # Bash script for running server
├── src/                    # Source code
│   ├── api/                # API implementation
│   │   ├── api.py          # FastAPI implementation
│   │   └── case_insights.py  # Case insights module
│   ├── data/               # Data handling modules
│   │   ├── data_generator.py  # Synthetic data generation
│   │   ├── data_processor.py  # Data preprocessing
│   │   └── merged_data.csv  # Processed data
│   ├── model/              # Model implementation
│   │   ├── case_model.pkl  # Trained model
│   │   ├── feature_importance.png  # Feature importance visualization
│   │   └── model_trainer.py  # Model training module
│   ├── utils/              # Utility functions
│   └── main.py             # Main workflow script
└── tests/                  # Test suite
    ├── test_api.py         # API endpoint tests
    └── test_prediction.py  # Prediction endpoint tests
```

## Components

- **Data Generation**: Synthetic case management data generation (`src/data/data_generator.py`)
- **Data Processing**: Preprocessing and feature engineering (`src/data/data_processor.py`)
- **Model Training**: Random Forest classifier for prediction (`src/model/model_trainer.py`) 
- **Case Insights**: AI agent that provides insights on case data (`src/api/case_insights.py`)
- **API Server**: FastAPI implementation for model and insights access (`src/api/api.py`)

## Installation

```bash
# Create conda environment
conda create -n ai-automation python=3.11 -y

# Activate the environment
conda activate ai-automation

# Install dependencies
pip install -r config/requirements.txt
```

## Usage

The application can be run using the provided entry point:

```bash
# Start the API server (default)
python app.py

# Generate synthetic data
python app.py --generate-data

# Train the model
python app.py --train-model

# Run analysis
python app.py --run-analysis

# Run the API server on a specific port
python app.py --run-server --port 8000
```

Alternatively, you can use the PowerShell scripts in the scripts directory:

```powershell
# Run the API server (Windows)
.\scripts\run_server.ps1

# Run with debug mode (Windows)
.\scripts\run_api_server.ps1 -Debug
```

Or bash scripts on Unix-like systems:

```bash
# Run the API server (Linux/macOS)
bash scripts/run_server.sh
```

## Testing

The project includes comprehensive tests for the API:

```bash
# Run API endpoint tests
python -m tests.test_api

# Run prediction endpoint tests
python -m tests.test_prediction
```

## Documentation

Detailed documentation is available in the docs directory:

- [API Setup](docs/API_SETUP.md) - Instructions for setting up and running the API
- [Developer Notes](docs/DEVELOPER_NOTES.md) - Technical notes for developers
- [Detailed Documentation](docs/README.md) - Comprehensive project documentation

### API Endpoints

- **GET /** - Welcome page and status check
- **POST /predict** - Make case resolution predictions
- **POST /insights** - Get insights from case data
- **GET /model-info** - Get information about the trained model

### Making Predictions

The prediction endpoint uses a Random Forest model trained on case management data. The model primarily considers the following features:
- Case type
- Case complexity
- Client age
- Client income level
- Days the case has been open
- Escalation status

Example request:

```json
{
  "case_type": "Family Law",
  "complexity": "Medium",
  "client_age": 35,
  "client_income_level": "Medium",
  "days_open": 30,
  "escalated": false
}
```

Example response:

```json
{
  "prediction": "Resolved",
  "probability": 0.792611113127238
}
```

### Getting Insights

Example request:

```json
{
  "insight_type": "common_case_types"
}
```

Valid insight types:
- `common_case_types`
- `resolution_factors`
- `assignee_performance`

## Testing

### Using curl

You can test the API using curl:

```bash
curl http://localhost:5000/
```

For prediction:

```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"case_type": "Family Law", "complexity": "Medium", "client_age": 35, "client_income_level": "Medium", "days_open": 30, "escalated": false}'
```

### Using the test scripts

The project includes Python test scripts to verify API functionality:

- `test_api.py` - Tests all API endpoints
- `test_prediction.py` - Focuses specifically on testing the prediction endpoint with various case scenarios

Run tests with:

```bash
python test_api.py
python test_prediction.py
```

## Project Structure

- `data_generator.py` - Generates synthetic case management data
- `data_processor.py` - Preprocesses data for model training
- `model_trainer.py` - Trains and evaluates the predictive model
- `case_insights.py` - Provides insights and analysis of case data
- `main.py` - Main script to run the complete workflow
- `api.py` - FastAPI implementation for model and insights access
- `run_server.ps1` - Primary script to run the API server
- `run_api_server.ps1` - Alternative script to run the API server
- `test_api.py` - Script to test all API endpoints
- `test_prediction.py` - Script to test the prediction endpoint 