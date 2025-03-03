# Developer Notes

This document contains technical notes and implementation details for the Case AI Analytics project, focusing on key fixes and design decisions.

## Prediction Endpoint Fix

### Issue: Feature Name Mismatch

The prediction endpoint in `api.py` was failing with the following error:
```
ValueError: The feature names should match those that were passed during fit.
Feature names unseen at fit time:
- assignee_Attorney_10
- assignee_Attorney_11
- assignee_Attorney_12
...
```

### Root Cause

The issue was occurring because:
1. The model was trained with a specific set of features
2. The prediction endpoint was attempting to create a DataFrame with different feature names
3. The scikit-learn model was expecting feature names to match exactly those used during training

### Solution Implemented

The fix involved several changes to the `predict` function in `api.py`:

1. **Access Model Feature Names**: Use the `feature_names_in_` attribute of the trained model to determine exactly which features the model expects.

2. **Direct Array Creation**: Instead of trying to create a DataFrame with matching columns, we create a numpy array with the exact number of features the model expects.

3. **Targeted Feature Setting**: We map each request field directly to the corresponding index in the feature array:
   - For numerical features (like age, resolution_days, escalated), we set values directly
   - For categorical features with one-hot encoding (like case_type, complexity, income_level), we set the matching one-hot feature to 1

4. **Debug Information**: Added detailed logging to print:
   - Request data
   - Model feature names
   - Input data shape before prediction
   - Prediction results

### Code Details

Key implementation aspects:

```python
# Get the model's expected feature count
n_features = model.n_features_in_ if hasattr(model, 'n_features_in_') else 4

# Create input data with the correct number of features
input_data = np.zeros((1, n_features))

# If the model has feature names, use them to map request fields
if hasattr(model, 'feature_names_in_'):
    feature_names = model.feature_names_in_
    
    # Map numerical features
    for feature, value in [
        ('age', request.client_age),
        ('escalated', 1 if request.escalated else 0),
        ('resolution_days', request.days_open if request.days_open is not None else 0)
    ]:
        if feature in feature_names:
            idx = np.where(feature_names == feature)[0][0]
            input_data[0, idx] = value
    
    # Map categorical features with one-hot encoding
    for prefix, value in [
        ('case_type_', request.case_type),
        ('complexity_', request.complexity),
        ('income_level_', request.client_income_level)
    ]:
        feature = f"{prefix}{value}"
        if feature in feature_names:
            idx = np.where(feature_names == feature)[0][0]
            input_data[0, idx] = 1
```

## Server Configuration

The API server has been configured to run on port 5000. This is defined in both server scripts:

1. `run_server.ps1` - The primary script that activates the conda environment and runs the server
2. `run_api_server.ps1` - An alternative script with more detailed configuration

Both scripts use `uvicorn` to run the FastAPI application:

```powershell
python -m uvicorn api:app --host 0.0.0.0 --port 5000
```

## Testing

Two test scripts have been created:

1. `test_api.py` - Tests all endpoints of the API
2. `test_prediction.py` - Focuses specifically on testing the prediction endpoint with various case scenarios

The test scripts are designed to be run after the server is started and provide immediate feedback on whether the API is functioning correctly.

## Future Improvements

Potential areas for future development:

1. **Feature Engineering**: Explore additional features that could improve prediction accuracy
2. **Model Versioning**: Implement a system to track model versions and facilitate A/B testing
3. **User Interface**: Develop a web-based UI for interacting with the API
4. **Data Visualization**: Add visualization capabilities to better understand model predictions
5. **Model Explanations**: Implement SHAP or LIME for explaining individual predictions 