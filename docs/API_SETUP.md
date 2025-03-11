# API Setup Guide

This guide details the setup and configuration of the Case Management API system.

## Current Architecture

The API is built with FastAPI and deployed on Render.com, providing:
- RESTful endpoints for case management
- AI-powered chatbot integration
- Real-time metrics and insights
- Secure environment variable management

## API Endpoints

### Base URL
```
https://case-management-ai.onrender.com/api
```

### Available Endpoints

1. **Status Check**
   ```
   GET /api
   Response: {"message": "Welcome to the Case Management API"}
   ```

2. **Case Data**
   ```
   GET /api/cases
   Response: Array of case objects
   ```

3. **System Metrics**
   ```
   GET /api/metrics
   Response: Current system metrics
   ```

4. **AI Insights**
   ```
   GET /api/insights
   Response: AI-generated insights
   ```

5. **Chat Interface**
   ```
   POST /api/chat
   Body: {"message": "Your question here"}
   Response: AI-generated response
   ```

## Local Development Setup

1. **Prerequisites**
   - Python 3.10+
   - pip package manager
   - Git

2. **Environment Setup**
   ```bash
   # Clone repository
   git clone https://github.com/your-username/case-management-ai.git
   cd case-management-ai

   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   .\venv\Scripts\activate   # Windows

   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Environment Variables**
   ```bash
   # Create .env file
   touch .env

   # Add required variables
   GEMINI_API_KEY=your_gemini_api_key
   OPENAI_API_KEY=your_openai_api_key  # Optional
   ENVIRONMENT=development
   ```

4. **Run Development Server**
   ```bash
   cd api
   uvicorn index:app --reload --port 8000
   ```

## Production Deployment (Render.com)

1. **Prerequisites**
   - Render.com account
   - GitHub repository access
   - API keys (Gemini/OpenAI)

2. **Configuration Files**
   ```bash
   # Procfile
   web: cd api && uvicorn index:app --host 0.0.0.0 --port $PORT

   # render.yaml
   services:
     - type: web
       name: case-management-api
       env: python
       buildCommand: pip install -r requirements.txt
       startCommand: cd api && uvicorn index:app --host 0.0.0.0 --port $PORT
       envVars:
         - key: PYTHON_VERSION
           value: 3.10.0
         - key: GEMINI_API_KEY
           sync: false
         - key: OPENAI_API_KEY
           sync: false
       healthCheckPath: /api
   ```

3. **Deployment Steps**
   - Connect repository to Render.com
   - Configure environment variables
   - Deploy service
   - Monitor health checks

## API Integration

### Frontend Integration
```python
# Example API client setup
import requests

API_BASE_URL = "https://case-management-ai.onrender.com/api"

def get_cases():
    response = requests.get(f"{API_BASE_URL}/cases")
    return response.json()

def chat_with_ai(message):
    response = requests.post(f"{API_BASE_URL}/chat", 
                           json={"message": message})
    return response.json()
```

### Error Handling
```python
def api_request(endpoint, method="GET", data=None):
    try:
        url = f"{API_BASE_URL}/{endpoint}"
        response = requests.request(method, url, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API Error: {str(e)}")
        return None
```

## Security Considerations

1. **API Keys**
   - Store in environment variables
   - Never commit to version control
   - Rotate regularly
   - Use secrets management in production

2. **Rate Limiting**
   - Implement per-client limits
   - Monitor usage patterns
   - Set up alerts for abuse

3. **Error Handling**
   - Sanitize error messages
   - Log security events
   - Implement retry logic

## Monitoring

1. **Health Checks**
   - Regular endpoint monitoring
   - Response time tracking
   - Error rate monitoring

2. **Logging**
   - Request/response logging
   - Error tracking
   - Performance metrics

3. **Alerts**
   - Service disruptions
   - High error rates
   - Resource utilization

## Testing

1. **Local Testing**
   ```bash
   # Run tests
   pytest tests/

   # Test specific endpoint
   curl http://localhost:8000/api
   ```

2. **Production Testing**
   ```bash
   # Test production endpoint
   curl https://case-management-ai.onrender.com/api

   # Test with authentication
   curl -H "Authorization: Bearer $API_KEY" \
        https://case-management-ai.onrender.com/api/cases
   ```

## Troubleshooting

1. **Common Issues**
   - API key configuration
   - CORS settings
   - Rate limiting
   - Connection timeouts

2. **Debug Tools**
   - FastAPI debug mode
   - Request logging
   - Error tracking
   - Performance monitoring

## Future Improvements

1. **Performance**
   - Response caching
   - Query optimization
   - Connection pooling

2. **Security**
   - OAuth implementation
   - API key rotation
   - Request validation

3. **Features**
   - Batch operations
   - Real-time updates
   - Advanced analytics 