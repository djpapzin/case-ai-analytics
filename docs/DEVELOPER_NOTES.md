# Developer Notes

## Technical Implementation Details

### AI Chatbot Implementation

#### Architecture
- Uses LangChain for chat functionality
- Supports multiple LLM providers:
  - Google Gemini (default, free)
  - OpenAI (fallback, paid)
- Maintains conversation history
- Integrates with case data API

#### Implementation Details
```python
# LLM Configuration
model_config = {
    'gemini': {
        'model': 'gemini-2.0-flash',
        'temperature': 0.7
    },
    'openai': {
        'model': 'gpt-3.5-turbo',
        'temperature': 0.7
    }
}

# Conversation Memory
memory = ConversationBufferMemory()

# API Integration
api_endpoints = {
    'cases': '/cases',
    'metrics': '/metrics',
    'insights': '/insights'
}
```

### Feature Mapping Fix

#### Issue
The prediction endpoint was experiencing feature name mismatches between the input data and the trained model. The model was trained with specific feature names, but the input data had different feature names, causing prediction failures.

#### Solution
1. Implemented a feature mapping system that maintains consistency between input features and model features
2. Added validation to ensure all required features are present in the input data
3. Created a mapping between input feature names and model feature names

#### Implementation Details
```python
# Feature mapping structure
feature_mapping = {
    'resolution_days': 0,
    'escalated': 1,
    'age': 3,
    'client_tenure_days': 4
}

# Input validation
required_features = ['case_type', 'complexity', 'client_age', 'client_income_level', 'days_open', 'escalated']
```

### Error Handling Improvements

#### Logging System
- Implemented structured logging for better debugging
- Added request/response logging for API endpoints
- Included model prediction details in logs
- Added chatbot interaction logging

#### Error Response Format
```python
{
    "error": "Feature validation failed",
    "details": "Missing required feature: client_age",
    "timestamp": "2024-03-14T12:00:00Z"
}
```

### Testing Framework

#### Test Structure
- `test_api.py`: Tests all API endpoints
  - Root endpoint validation
  - Prediction endpoint functionality
  - Insights endpoint response format
- `test_prediction.py`: Focused testing of prediction endpoint
  - Feature validation
  - Response format validation
  - Error handling
- `test_chatbot.py`: Tests AI assistant functionality
  - Model initialization
  - Conversation memory
  - API integration
  - Response generation

#### Test Cases
```python
chatbot_test_cases = [
    {
        "input": "Show me current case metrics",
        "expected_api_calls": ["metrics"],
        "validate_response": True
    },
    {
        "input": "Analyze recent trends",
        "expected_api_calls": ["cases", "insights"],
        "validate_response": True
    }
]
```

## Server Configuration

### Port Configuration
- Default port: 8000
- Configurable through command line arguments
- Environment variable support: `PORT`

### Debug Mode
- Enabled with `--debug` flag
- Provides detailed logging
- Shows stack traces for errors

## Model Details

### Feature Engineering
1. **Input Features**:
   - Case type (categorical)
   - Complexity level (categorical)
   - Client age (numerical)
   - Client income level (categorical)
   - Days open (numerical)
   - Escalation status (boolean)

2. **Feature Processing**:
   - Categorical encoding
   - Numerical normalization
   - Feature validation

### Model Architecture
- Random Forest Classifier
- Hyperparameters:
  - n_estimators: 100
  - max_depth: 10
  - random_state: 42

## API Endpoints

### Prediction Endpoint
- **URL**: `/predict`
- **Method**: POST
- **Input Format**:
```json
{
    "case_type": "string",
    "complexity": "string",
    "client_age": "integer",
    "client_income_level": "string",
    "days_open": "integer",
    "escalated": "boolean"
}
```
- **Output Format**:
```json
{
    "prediction": "string",
    "probability": "float"
}
```

### Insights Endpoint
- **URL**: `/insights`
- **Method**: POST
- **Input Format**:
```json
{
    "insight_type": "string"
}
```
- **Output Format**:
```json
{
    "insights": {
        "case_types": {
            "type": "count"
        },
        "resolution_factors": {
            "factor": "impact"
        }
    }
}
```

### Chatbot Integration
- **Memory Management**: Conversation history stored in memory
- **Context Integration**: Real-time data fetching
- **Error Handling**: Graceful fallback between models
- **Response Generation**: Natural language processing

## Future Improvements

### Feature Engineering
1. Add more sophisticated feature engineering
2. Implement feature importance analysis
3. Add feature selection based on importance

### Model Versioning
1. Implement model versioning system
2. Add model performance tracking
3. Create model comparison tools

### User Interface
1. Develop web interface for predictions
2. Add visualization dashboard
3. Implement user authentication
4. Enhance chatbot UI/UX
5. Add conversation export functionality

### Data Visualization
1. Add case type distribution charts
2. Implement resolution time analysis
3. Create performance metrics dashboard

### Model Explanations
1. Add SHAP value explanations
2. Implement feature importance visualization
3. Create case-specific explanation reports

### AI Assistant Enhancements
1. Add support for more LLM providers
2. Implement caching for API responses
3. Add custom prompt templates
4. Enhance conversation memory management
5. Implement rate limiting and usage tracking

## Troubleshooting Guide

### Common Issues

1. **Feature Name Mismatch**
   - Check feature_mapping.json
   - Verify input data format
   - Validate feature names in model

2. **Model Loading Errors**
   - Verify model file exists
   - Check model version compatibility
   - Validate model format

3. **API Connection Issues**
   - Check port availability
   - Verify server status
   - Check firewall settings

4. **AI Model Issues**
   - Check API key configuration
   - Verify model availability
   - Monitor rate limits
   - Check for model-specific errors

### Debug Mode
Enable debug mode for detailed logging:
```bash
python app.py --debug
```

### Log Files
- Server logs: `logs/server.log`
- Model logs: `logs/model.log`
- API logs: `logs/api.log`
- Chatbot logs: `logs/chatbot.log` 