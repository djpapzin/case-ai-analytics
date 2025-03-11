# Cloud Deployment Guide

This document provides instructions for deploying the Case Management AI system to cloud platforms.

## Current Deployment

The system is currently deployed to:
- **Backend API**: [Render.com](https://case-management-ai.onrender.com/api)
- **Frontend Dashboard**: [Streamlit Cloud](https://case-management-ai.streamlit.app/)

## Deployment Architecture

![Deployment Architecture](https://mermaid.ink/img/pako:eNp1kU1PwzAMhv9KlBMgdT3QA4deEBJiB8QOcHATN_XWfMhxJqaq_51kLYxNiJzs1_bzOvZJVVYTVWrDPTk0gZ7RdQQfELyHBwfbDRqCJwKLPVmEDRwJWrKAHp0lCOQ9eXDYgcEGHQxkCQJ6h4E6-Aw9GWjJwRsE9I4CtBZbCOSxhxZNgJ4GGKAnD1_kYIcNDOixhY4G-KYBPmCLe_IwkMc9tGTxSAO8o8OWPJ7Jw4E8fKHBDgcYyGJHFr_Qk4WBHB7JwRYDvJGDIzk4UQ8HsniCgQJ8UoAjBXhBgwYDvKLBb_LwjBYDvKHBE1k8UYBXMtBTgANZOJLBb_LwQh5eyOErWRjI4xM5-CAPf1RpVeRZnhVFnhd5Vhb5vJwVZVmWs3JWlnlWzIu8yMrZPC_nZTYv8qLMy-JfQnlWFkU2z4vpVTbJq2xRZNPFYjGdTBfT6WKymM4W_wFKspTl?type=png)

## Backend Deployment (Render.com)

### Prerequisites
- A Render.com account
- Git repository with your code

### Configuration Files
The following files are required for Render.com deployment:

1. **Procfile**
   ```
   web: cd api && uvicorn index:app --host 0.0.0.0 --port $PORT
   ```

2. **render.yaml**
   ```yaml
   services:
     - type: web
       name: case-management-ai
       env: python
       buildCommand: pip install -r requirements.txt
       startCommand: cd api && uvicorn index:app --host 0.0.0.0 --port $PORT
       envVars:
         - key: PYTHON_VERSION
           value: 3.10.0
         - key: OPENAI_API_KEY
           sync: false
         - key: GOOGLE_API_KEY
           sync: false
       autoDeploy: true
       healthCheckPath: /api
       plan: free
   ```

3. **runtime.txt**
   ```
   python-3.10.0
   ```

### Deployment Steps

1. **Connect Repository**
   - Log in to Render.com
   - Go to Dashboard and click "New +"
   - Select "Web Service"
   - Connect your GitHub/GitLab repository

2. **Configure Service**
   - Name: case-management-ai
   - Environment: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `cd api && uvicorn index:app --host 0.0.0.0 --port $PORT`

3. **Set Environment Variables**
   - PYTHON_VERSION: 3.10.0
   - OPENAI_API_KEY: Your OpenAI API key (if using OpenAI)
   - GOOGLE_API_KEY: Your Google API key (if using Gemini)

4. **Deploy**
   - Click "Create Web Service"
   - Wait for the build and deployment to complete

5. **Verify Deployment**
   - Visit the provided URL + "/api" to check if the API is running
   - Example: https://case-management-ai.onrender.com/api

## Frontend Deployment (Streamlit Cloud)

### Prerequisites
- A Streamlit Cloud account
- Git repository with your code

### Configuration Files

1. **requirements.txt**
   Ensure it includes all necessary packages:
   ```
   streamlit
   requests
   pandas
   plotly
   ```

2. **streamlit/config.toml**
   ```toml
   [theme]
   primaryColor = "#1E88E5"
   backgroundColor = "#FFFFFF"
   secondaryBackgroundColor = "#F0F2F6"
   textColor = "#262730"
   font = "sans serif"
   ```

### Deployment Steps

1. **Connect Repository**
   - Log in to Streamlit Cloud (https://share.streamlit.io/)
   - Click "New app"
   - Connect your GitHub/GitLab repository

2. **Configure App**
   - Main file path: `app/dashboard.py` (adjust to your actual path)
   - Python version: 3.10
   - Add any required secrets (API keys, etc.)

3. **Advanced Settings**
   - Set custom theme if needed
   - Configure memory/CPU requirements

4. **Deploy**
   - Click "Deploy"
   - Wait for the build and deployment to complete

5. **Verify Deployment**
   - Visit the provided URL to check if the dashboard is running
   - Example: https://case-management-ai.streamlit.app/

## Connecting Frontend to Backend

The frontend dashboard needs to communicate with the backend API. This is configured in the dashboard code:

```python
# Example configuration in dashboard.py
API_URL = "https://case-management-ai.onrender.com/api"
```

Ensure the API URL is correctly set in your dashboard code.

## Monitoring and Maintenance

### Render.com Monitoring
- View logs in the Render.com dashboard
- Set up alerts for service disruptions
- Monitor resource usage

### Streamlit Cloud Monitoring
- View app metrics in the Streamlit Cloud dashboard
- Check app logs for errors
- Monitor app performance

## Troubleshooting

### Common Issues

1. **API Connection Errors**
   - Check if the API is running
   - Verify CORS settings in the API
   - Check network connectivity

2. **Deployment Failures**
   - Check build logs for errors
   - Verify dependencies in requirements.txt
   - Check for syntax errors in code

3. **Performance Issues**
   - Monitor resource usage
   - Optimize database queries
   - Implement caching where appropriate

## Future Improvements

1. **Scaling**
   - Upgrade to paid plans for better performance
   - Implement database caching
   - Use CDN for static assets

2. **Security**
   - Add authentication to API
   - Implement rate limiting
   - Set up HTTPS with custom domain

3. **CI/CD**
   - Set up automated testing
   - Implement blue-green deployments
   - Add deployment notifications 