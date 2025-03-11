# Case AI Analytics

ML-powered system for predicting case outcomes and extracting insights from case management data. Uses Random Forest for resolution prediction and provides analysis on case types, resolution factors, and assignee performance. Includes FastAPI server for API access and an AI-powered chatbot interface.

## Live System
- **Dashboard**: [Live Demo](https://ai-powered-legal-case-management-system.streamlit.app/)
- **API**: [Production Endpoint](https://case-management-ai.onrender.com/api)

## Project Overview

This project consists of three main parts:
1. **Machine Learning Model**: Predicts case outcomes based on case management system data.
2. **AI Agent for Case Insights**: Provides actionable insights from the case management data.
3. **Interactive AI Assistant**: Chatbot interface for natural language interactions with the system.
4. **Cloud Deployment**: Backend API on Render.com and frontend dashboard on Streamlit Cloud.

## Components

- **Data Generation**: Synthetic case management data generation (`data_generator.py`)
- **Data Processing**: Preprocessing and feature engineering (`data_processor.py`)
- **Model Training**: Random Forest classifier for prediction (`model_trainer.py`) 
- **Case Insights**: AI agent that provides insights on case data (`case_insights.py`)
- **API Server**: FastAPI implementation for model and insights access (`api/index.py`)
- **AI Chatbot**: LangChain-based chatbot for interactive case analysis (`src/agent/case_chatbot.py`)
- **Cloud Deployment**: Configuration for Render.com and Streamlit Cloud deployment

## Live Deployment

- **Dashboard**: [Streamlit Cloud Dashboard](https://ai-powered-legal-case-management-system.streamlit.app/)
- **API**: [Render API Endpoint](https://case-management-ai.onrender.com/api)

### API Endpoints

- **GET /api** - Welcome page and status check
- **GET /api/cases** - Retrieve case data
- **GET /api/metrics** - Get current system metrics
- **GET /api/insights** - Get insights from case data
- **POST /api/chat** - Interact with the AI chatbot

## Deployment

### Backend API (Render.com)
The FastAPI backend is deployed on Render.com for reliable operation:
- **Production URL**: https://case-management-ai.onrender.com/api
- **Configuration**: 
  - Uses `Procfile` for process management
  - `render.yaml` for service configuration
  - `runtime.txt` for Python version
- **Features**:
  - Improved cold start times
  - Better Python process handling
  - Automatic scaling
  - Health monitoring
- **Endpoints**:
  - `GET /api` - Welcome page and status check
  - `GET /cases` - Retrieve case data
  - `GET /metrics` - Get current system metrics
  - `GET /insights` - Get AI-powered insights
  - `POST /chat` - Interact with AI chatbot

### Frontend Dashboard (Streamlit)
The Streamlit dashboard is deployed on Streamlit Cloud:
- **Live URL**: https://ai-powered-legal-case-management-system.streamlit.app/
- **Features**:
  - Real-time integration with Render.com API
  - Interactive visualizations
  - AI chatbot interface with Gemini API
  - Secure environment variable management
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
1. **Render.com Deployment**:
   - Push code to GitHub
   - Connect repository to Render.com
   - Configure build settings
   - Set environment variables
   - Deploy using GitHub integration

2. **Streamlit Deployment**:
   - Push code to GitHub
   - Connect repository to Streamlit Cloud
   - Configure with requirements.txt
   - Set up `.streamlit/secrets.toml`
   - Set environment variables for API keys

## Installation

```bash
# Create conda environment
conda create -n ai-automation python=3.12 -y

# Activate the environment
conda activate ai-automation

# Install dependencies
pip install -r requirements.txt
```

## Usage

The API server can be started using the following command and will be available at port 8000:

```bash
cd api && python -m uvicorn index:app --host 0.0.0.0 --port 8000
```

To run the Streamlit dashboard locally:

```bash
python -m streamlit run dashboard.py
```

### Server Scripts

- **run_api.bat** - Runs the API server on Windows
- **Procfile** - Configuration for Render.com deployment

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

## Cloud Deployment

### Backend Deployment (Render.com)

The FastAPI backend is deployed on Render.com, providing:
- 24/7 availability with improved reliability
- Automatic scaling
- Better Python support
- Improved cold start times
- Long-running process handling
- Secure API endpoints

Configuration files:
- `Procfile` - Defines the command to start the server
- `render.yaml` - Defines the service configuration
- `runtime.txt` - Specifies the Python version

### Frontend Deployment (Streamlit Cloud)

The Streamlit dashboard is deployed on Streamlit Cloud, providing:
- Interactive web interface
- Real-time data visualization
- Secure access to the API
- Integrated AI chatbot with Gemini API
- Environment variable management through secrets

## Testing

### Using curl

You can test the API using curl:

```bash
curl https://case-management-ai.onrender.com/api
```

For the cases endpoint:

```bash
curl https://case-management-ai.onrender.com/api/cases
```

For the chatbot:

```bash
curl -X POST https://case-management-ai.onrender.com/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "How many active cases do we have?"}'
```

## Project Structure

- `api/index.py` - FastAPI implementation for model and insights access
- `src/agent/case_chatbot.py` - AI-powered chatbot interface
- `dashboard.py` - Streamlit dashboard with integrated AI assistant
- `Procfile` - Render deployment configuration
- `render.yaml` - Render service definition
- `runtime.txt` - Python version specification
- `requirements.txt` - Python dependencies 