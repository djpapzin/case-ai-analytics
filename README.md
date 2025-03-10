# Case Management AI System

An AI-powered legal case management system that helps law firms and legal departments manage cases more efficiently through predictive analytics and automated insights.

## Live Demo 🚀
- **Dashboard**: [AI-Powered Legal Case Management System](https://ai-powered-legal-case-management-system.streamlit.app/)
- **API**: [Case Management API](https://ai-automation-q2fcum39s-djpapzins-projects.vercel.app)

## Features

- 🤖 AI-powered case outcome prediction
- 📊 Interactive dashboard with real-time insights
- 📈 Case analytics and trend analysis
- 🔄 Automated case status updates
- 📋 Case priority management
- 👥 Resource allocation suggestions
- 💬 AI Assistant chatbot for case insights
- 🔄 Automatic model fallback (Gemini/OpenAI)

## Architecture

### Backend
- FastAPI for REST API (deployed on Vercel)
- Random Forest model for predictions
- SQLite database for data storage
- Python-based data processing pipeline
- LangChain for AI chat capabilities

### Frontend
- Streamlit dashboard (deployed on Streamlit Cloud)
- Interactive data visualization
- Real-time updates
- Responsive design
- Integrated AI chatbot interface

## Deployment

### Backend API (Vercel)
The FastAPI backend is deployed on Vercel for serverless operation:
- Production API: https://ai-automation-q2fcum39s-djpapzins-projects.vercel.app
- Endpoints:
  - `/cases` - Get case data
  - `/metrics` - Get system metrics
  - `/insights` - Get AI-powered insights

### Frontend Dashboard (Streamlit)
The Streamlit dashboard is deployed on Streamlit Cloud:
- Live Dashboard: https://ai-powered-legal-case-management-system.streamlit.app/
- Features real-time integration with the Vercel API
- Includes AI chatbot interface

## Getting Started

### Prerequisites
- Python 3.12+
- pip (Python package manager)
- Google Gemini API key (free) or OpenAI API key (paid)
- Vercel account (for API deployment)
- Streamlit account (for dashboard deployment)

### API Key Setup

1. **Google Gemini API (Recommended - Free)**
   - Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Create a new API key
   - Copy the key to your `.env` file as `GEMINI_API_KEY`
   - Uses the latest `gemini-2.0-flash` model

2. **OpenAI API (Optional - Paid)**
   - Visit [OpenAI API Keys](https://platform.openai.com/settings/organization/api-keys)
   - Create a new API key
   - Copy the key to your `.env` file as `OPENAI_API_KEY`

3. **Environment Setup**
   - Copy `.env.example` to `.env`
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

5. Start the API server:
```bash
python app.py --run-server
```

6. Run the dashboard:
```bash
python -m streamlit run dashboard.py
```

The dashboard will be available at http://localhost:8501

## Project Structure

```
case-management-ai/
├── src/
│   ├── api/            # FastAPI endpoints
│   ├── data/           # Data processing and generation
│   ├── model/          # ML model implementation
│   └── utils/          # Helper functions
├── docs/               # Documentation
├── tests/              # Test files
├── config/             # Configuration files
├── scripts/            # Utility scripts
├── app.py             # Main application
├── dashboard.py       # Streamlit dashboard
└── requirements.txt   # Python dependencies
```

## Usage

1. Access the dashboard at http://localhost:8501
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
- Powered by scikit-learn 