# Case AI Analytics

ML-powered system for predicting case outcomes and extracting insights from case management data. Uses Random Forest for resolution prediction and provides analysis on case types, resolution factors, and assignee performance. Includes FastAPI server for API access.

## Project Overview

This project consists of two main parts:
1. **Machine Learning Model**: Predicts case outcomes based on case management system data.
2. **AI Agent for Case Insights**: Provides actionable insights from the case management data.

## Components

- **Data Generation**: Synthetic case management data generation (`data_generator.py`)
- **Data Processing**: Preprocessing and feature engineering (`data_processor.py`)
- **Model Training**: Random Forest classifier for prediction (`model_trainer.py`) 
- **Case Insights**: AI agent that provides insights on case data (`case_insights.py`)
- **API Server**: FastAPI implementation for model and insights access (`api.py`)

## Installation

```bash
# Create conda environment
conda create -n ai-automation python=3.11 -y

# Activate the environment
conda activate ai-automation

# Install dependencies
pip install pandas numpy scikit-learn matplotlib seaborn faker fastapi uvicorn
```

## Usage

The API server can be started using the provided PowerShell scripts and will be available at port 8000.

### API Endpoints

- **GET /** - Welcome page and status check
- **POST /predict** - Make case resolution predictions
- **POST /insights** - Get insights from case data
- **GET /model-info** - Get information about the trained model

### Making Predictions

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

You can test the API using curl:

```bash
curl http://154.0.164.254:8000/
```

For prediction:

```bash
curl -X POST http://154.0.164.254:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"case_type": "Family Law", "complexity": "Medium", "client_age": 35, "client_income_level": "Medium", "days_open": 30, "escalated": false}'
```

## Project Structure

- `data_generator.py` - Generates synthetic case management data
- `data_processor.py` - Preprocesses data for model training
- `model_trainer.py` - Trains and evaluates the predictive model
- `case_insights.py` - Provides insights and analysis of case data
- `main.py` - Main script to run the complete workflow
- `api.py` - FastAPI implementation for model and insights access
- `run_api_server.ps1` - Script to run the API server 