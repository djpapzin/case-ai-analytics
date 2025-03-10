# Case AI Analytics

ML-powered system for predicting case outcomes and extracting insights from case management data. Uses Random Forest for resolution prediction and provides analysis on case types, resolution factors, and assignee performance. Includes FastAPI server for API access and an AI-powered chatbot interface.

## Live System
- **Dashboard**: [Live Demo](https://ai-powered-legal-case-management-system.streamlit.app/)
- **API**: [Production Endpoint](https://ai-automation-q2fcum39s-djpapzins-projects.vercel.app)

## Project Overview

This project consists of three main parts:
1. **Machine Learning Model**: Predicts case outcomes based on case management system data.
2. **AI Agent for Case Insights**: Provides actionable insights from the case management data.
3. **Interactive AI Assistant**: Chatbot interface for natural language interactions with the system.

## Components

- **Data Generation**: Synthetic case management data generation (`data_generator.py`)
- **Data Processing**: Preprocessing and feature engineering (`data_processor.py`)
- **Model Training**: Random Forest classifier for prediction (`model_trainer.py`) 
- **Case Insights**: AI agent that provides insights on case data (`case_insights.py`)
- **API Server**: FastAPI implementation for model and insights access (`api.py`)
- **AI Chatbot**: LangChain-based chatbot for interactive case analysis (`case_chatbot.py`)

## Deployment

### Backend API (Vercel)
The FastAPI backend is deployed on Vercel for serverless operation:
- **Production URL**: https://ai-automation-q2fcum39s-djpapzins-projects.vercel.app
- **Configuration**: Uses `vercel.json` for build and route settings
- **Dependencies**: Optimized requirements.txt for Vercel's size limits
- **Endpoints**:
  - `GET /` - Welcome page and status check
  - `GET /cases` - Retrieve case data
  - `GET /metrics` - Get current system metrics
  - `GET /insights` - Get AI-powered insights

### Frontend Dashboard (Streamlit)
The Streamlit dashboard is deployed on Streamlit Cloud:
- **Live URL**: https://ai-powered-legal-case-management-system.streamlit.app/
- **Features**:
  - Real-time integration with Vercel API
  - Interactive visualizations
  - AI chatbot interface
  - Case analytics and insights

### Development Setup
For local development:
```bash
# Install dependencies
pip install -r requirements.txt

# Run API locally
uvicorn api.main:app --reload

# Run dashboard locally
streamlit run dashboard.py
```

### Production Setup
1. **Vercel Deployment**:
   - Push code to GitHub
   - Connect repository to Vercel
   - Configure build settings via vercel.json
   - Deploy using Vercel CLI or GitHub integration

2. **Streamlit Deployment**:
   - Push code to GitHub
   - Connect repository to Streamlit Cloud
   - Configure with requirements.txt
   - Set environment variables for API keys

## Installation

```bash
# Create conda environment
conda create -n ai-automation python=3.11 -y

# Activate the environment
conda activate ai-automation

# Install dependencies
pip install pandas numpy scikit-learn matplotlib seaborn faker fastapi uvicorn langchain langchain-google-genai langchain-openai python-dotenv
```

## Usage

The API server can be started using the provided PowerShell scripts and will be available at port 8000.

### Server Scripts

- **run_server.ps1** - Runs the API server with the Conda environment activated
- **run_api_server.ps1** - Alternative script to run the server with more detailed configuration

### API Endpoints

- **GET /** - Welcome page and status check
- **POST /predict** - Make case resolution predictions
- **GET /insights** - Get insights from case data
- **GET /metrics** - Get current system metrics
- **GET /cases** - Retrieve case data
- **GET /model-info** - Get information about the trained model

### AI Assistant

The system includes an AI-powered chatbot that provides:
- Natural language interactions with case data
- Real-time analysis and insights
- Performance metric interpretations
- Trend identification
- Actionable recommendations

The chatbot supports two language models:
1. **Google Gemini (Default - Free)**
   - Uses the `gemini-2.0-flash` model
   - Recommended for most users
   - Requires Gemini API key

2. **OpenAI (Fallback - Paid)**
   - Uses GPT-3.5 Turbo
   - Optional fallback option
   - Requires OpenAI API key

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
curl http://localhost:8000/
```

For prediction:

```bash
curl -X POST http://localhost:8000/predict \
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
- `case_chatbot.py` - AI-powered chatbot interface
- `main.py` - Main script to run the complete workflow
- `api.py` - FastAPI implementation for model and insights access
- `dashboard.py` - Streamlit dashboard with integrated AI assistant
- `run_server.ps1` - Primary script to run the API server
- `run_api_server.ps1` - Alternative script to run the API server
- `test_api.py` - Script to test all API endpoints
- `test_prediction.py` - Script to test the prediction endpoint 