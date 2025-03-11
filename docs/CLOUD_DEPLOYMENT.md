# Cloud Deployment Guide

This guide details the deployment process for the Case Management AI System using Render.com and Streamlit Cloud.

## Current Architecture

### Backend (Render.com)
- FastAPI application deployed on Render.com
- Production URL: https://case-management-ai.onrender.com/api
- API Documentation: https://case-management-ai.onrender.com/docs
- Advantages over previous serverless setup:
  - Better Python support
  - Improved cold start times
  - Reliable long-running process handling
  - Automatic scaling
  - Built-in health monitoring

### Frontend (Streamlit Cloud)
- Streamlit dashboard deployed on Streamlit Cloud
- Production URL: https://ai-powered-legal-case-management-system.streamlit.app/
- Features:
  - Real-time connection to Render.com API
  - Interactive visualizations
  - Integrated Gemini API chatbot
  - Secure environment variable management

## Deployment Steps

### Backend Deployment (Render.com)

1. **Prerequisites**
   - GitHub account with repository access
   - Render.com account
   - Google Gemini API key
   - OpenAI API key (optional fallback)

2. **Render.com Setup**
   ```bash
   # Required files in repository
   Procfile              # Process management
   render.yaml           # Service configuration
   runtime.txt          # Python version
   requirements.txt     # Dependencies
   ```

3. **Configuration Steps**
   - Log in to Render.com
   - Create new Web Service
   - Connect GitHub repository
   - Configure build settings:
     - Name: case-management-api
     - Environment: Python
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `cd api && uvicorn index:app --host 0.0.0.0 --port $PORT`

4. **Environment Variables**
   ```
   GEMINI_API_KEY=your_gemini_api_key
   OPENAI_API_KEY=your_openai_api_key (optional)
   ENVIRONMENT=production
   ```

5. **Health Monitoring**
   - Set up health check endpoint: `/api`
   - Configure automatic restarts
   - Enable error notifications

### Frontend Deployment (Streamlit Cloud)

1. **Prerequisites**
   - GitHub account with repository access
   - Streamlit Cloud account
   - API keys for LLM services

2. **Streamlit Configuration**
   ```toml
   # .streamlit/secrets.toml
   GEMINI_API_KEY = "your_gemini_api_key"
   OPENAI_API_KEY = "your_openai_api_key"  # Optional
   API_URL = "https://case-management-ai.onrender.com/api"
   ```

3. **Deployment Steps**
   - Log in to Streamlit Cloud
   - Connect GitHub repository
   - Set main file path: `dashboard.py`
   - Configure secrets through Streamlit Cloud UI
   - Deploy application

4. **Environment Management**
   - Local development: Use `.env` file
   - Production: Use Streamlit secrets
   - Never commit API keys to repository

## Monitoring and Maintenance

### Backend (Render.com)
- Monitor service health through Render dashboard
- Check application logs for errors
- Monitor cold start performance
- Set up usage alerts

### Frontend (Streamlit)
- Monitor application through Streamlit Cloud
- Check error logs
- Monitor user sessions
- Track API response times

## Troubleshooting

### Common Issues

1. **Cold Starts**
   - Solution: Render.com always-on instance
   - Monitor startup times
   - Optimize initialization code

2. **API Timeouts**
   - Check Render.com service logs
   - Verify API endpoint health
   - Monitor response times

3. **Environment Variables**
   - Verify secrets in Streamlit Cloud
   - Check Render.com environment variables
   - Ensure API keys are valid

4. **Deployment Failures**
   - Check build logs
   - Verify dependencies
   - Test locally before deployment

## Security Considerations

1. **API Keys**
   - Use environment variables
   - Never commit secrets
   - Rotate keys regularly

2. **CORS Configuration**
   - Configure allowed origins
   - Implement rate limiting
   - Set up request validation

3. **Monitoring**
   - Set up error alerting
   - Monitor API usage
   - Track performance metrics

## Future Improvements

1. **Performance**
   - Implement caching
   - Optimize cold starts
   - Add CDN for static assets

2. **Reliability**
   - Set up automated backups
   - Implement blue-green deployment
   - Add failover strategies

3. **Security**
   - Add authentication
   - Implement rate limiting
   - Enhance monitoring 