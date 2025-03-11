# Case Management AI System

An AI-powered legal case management system that helps law firms and legal departments manage cases more efficiently through predictive analytics and automated insights.

## Live Demo 🚀
- **Dashboard**: [AI-Powered Legal Case Management System](https://ai-powered-legal-case-management-system.streamlit.app)
- **API**: [Case Management API](https://case-management-ai.onrender.com/api)

## Features

- 🤖 AI-powered case outcome prediction
- 📊 Interactive dashboard with real-time insights
- 📈 Case analytics and trend analysis
- 🔄 Automated case status updates
- 📋 Case priority management
- 👥 Resource allocation suggestions
- 💬 AI Assistant chatbot for case insights
- 🔄 Automatic model fallback (Gemini/OpenAI)
- ☁️ Cloud-based deployment with Render and Streamlit Cloud

## Architecture

### Backend
- FastAPI for REST API
- Random Forest model for predictions
- SQLite database for data storage
- Python-based data processing pipeline
- LangChain for AI chat capabilities
- Deployed on Render.com for reliable 24/7 availability
- Improved cold start times and Python process handling

### Frontend
- Streamlit dashboard
- Interactive data visualization
- Real-time updates
- Responsive design
- Integrated AI chatbot interface with Gemini API
- Environment variable management through Streamlit secrets
- Hosted on Streamlit Cloud

## Live Demo

- **Dashboard**: [Streamlit Cloud Dashboard](https://case-management-ai.streamlit.app/)
- **API**: [Render API Endpoint](https://case-management-ai.onrender.com/api)

## Cloud Deployment

The system is deployed using a modern cloud architecture:

### Backend (Render.com)
- FastAPI application deployed on Render.com
- Migrated from Vercel for better Python support and reliability
- Automatic scaling based on demand
- Continuous deployment from GitHub
- Environment variables for API keys
- Health checks and monitoring
- Improved cold start times
- Better handling of long-running Python processes

### Frontend (Streamlit Cloud)
- Streamlit dashboard hosted on Streamlit Cloud
- Automatic updates from GitHub repository
- Custom domain configuration
- Responsive design for all devices
- Secure environment variable management
- Integrated AI chatbot with Gemini API

For detailed deployment instructions, see [Cloud Deployment Guide](docs/CLOUD_DEPLOYMENT.md).

## Getting Started

### Prerequisites
- Python 3.10+
- pip (Python package manager)
- Google Gemini API key (free) or OpenAI API key (paid)
- Render.com account (for API deployment)
- Streamlit account (for dashboard deployment)

### API Key Setup

1. **Google Gemini API (Recommended - Free)**
   - Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Create a new API key
   - Copy the key to your `.env` file as `GEMINI_API_KEY`
   - For production, add to Streamlit secrets
   - Uses the latest `gemini-pro` model

2. **OpenAI API (Optional - Paid)**
   - Visit [OpenAI API Keys](https://platform.openai.com/settings/organization/api-keys)
   - Create a new API key
   - Copy the key to your `.env` file as `OPENAI_API_KEY`

3. **Environment Setup**
   - Copy `.env.example` to `.env` for local development
   - Create `.streamlit/secrets.toml` for production
   - Add at least one API key (Gemini recommended)
   - The system will automatically use available keys based on the following priority:
     1. Gemini (default - free)
     2. OpenAI (fallback - paid)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/djpapzin/case-management-ai.git
cd case-management-ai
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Generate sample data:
```bash
python app.py --generate-data
```

4. Train the model:
```bash
python app.py --train-model
```

5. Start the API server locally:
```bash
cd api && python -m uvicorn index:app --host 0.0.0.0 --port 8000
```

6. Run the dashboard locally:
```bash
python -m streamlit run dashboard.py
```

The dashboard will be available at http://localhost:8501

## Deployment

### Backend Deployment (Render.com)

1. Fork or clone this repository to your GitHub account
2. Sign up for [Render.com](https://render.com/)
3. Create a new Web Service and connect your GitHub repository
4. Configure the service:
   - Name: case-management-api
   - Environment: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `cd api && uvicorn index:app --host 0.0.0.0 --port $PORT`
5. Add environment variables:
   - GEMINI_API_KEY: Your Google Gemini API key
   - OPENAI_API_KEY: Your OpenAI API key (optional)
6. Deploy and monitor the service
7. Note the provided URL for API access

### Frontend Deployment (Streamlit Cloud)

1. Sign up for [Streamlit Cloud](https://streamlit.io/cloud)
2. Connect your GitHub repository
3. Configure the app:
   - Main file path: `dashboard.py`
   - Create `.streamlit/secrets.toml` with required API keys
4. Deploy and monitor the application
5. Access your dashboard through the provided URL

## Project Structure

```
case-management-ai/
├── api/               # FastAPI backend
│   ├── index.py       # Main API file
│   └── vercel.py      # Vercel configuration
├── src/
│   ├── agent/         # AI agent implementation
│   ├── data/          # Data processing and generation
│   ├── model/         # ML model implementation
│   └── utils/         # Helper functions
├── docs/              # Documentation
├── tests/             # Test files
├── dashboard.py       # Streamlit dashboard
├── Procfile           # Render deployment configuration
├── render.yaml        # Render service definition
├── runtime.txt        # Python version specification
└── requirements.txt   # Python dependencies
```

## Usage

1. Access the dashboard at https://case-management-ai.streamlit.app/ or http://localhost:8501 locally
2. Use the sidebar filters to analyze specific case types
3. View real-time metrics and insights
4. Use the AI Assistant tab for interactive case analysis
5. Export reports as needed

### AI Assistant Features

The integrated AI chatbot provides:
- Real-time case analysis
- Performance metrics interpretation
- Trend identification
- Actionable recommendations
- Natural language interactions

### Dashboard Preview

![Case Management Dashboard](docs/images/demo.jpeg)

*The dashboard provides real-time metrics, key insights, and interactive visualizations for case management.*

## Development

### Running Tests
```bash
python -m pytest tests/
```

### Code Style
We follow PEP 8 guidelines. Run the linter:
```bash
flake8 .
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Thanks to all contributors
- Built with Python, FastAPI, and Streamlit
- Powered by scikit-learn and LangChain
- Hosted on Render.com and Streamlit Cloud 