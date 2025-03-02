from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import pickle
import os
from typing import List, Dict, Any, Optional
import json
import uvicorn
import numpy as np

# Import project modules
from data_generator import generate_synthetic_data
from data_processor import preprocess_data
from model_trainer import train_evaluate_model
from case_insights import CaseInsights

# Initialize FastAPI app
app = FastAPI(
    title="Case Management AI API",
    description="API for case management prediction model and insights",
    version="1.0.0"
)

# Define request/response models
class PredictionRequest(BaseModel):
    case_type: str
    complexity: str
    client_age: int
    client_income_level: str
    days_open: Optional[int] = None
    escalated: bool = False

class PredictionResponse(BaseModel):
    prediction: str
    probability: float
    
class InsightType(BaseModel):
    insight_type: str  # One of: "common_case_types", "resolution_factors", "assignee_performance"

# Global variables to store model and data
model = None
insights_agent = None
merged_data = None
feature_mapping = {}

# Event handler for startup
@app.on_event("startup")
async def startup_event():
    global model, insights_agent, merged_data, feature_mapping
    
    # Check if a saved model exists, otherwise generate and train
    if os.path.exists("case_model.pkl"):
        print("Loading existing model...")
        with open("case_model.pkl", "rb") as f:
            model = pickle.load(f)
        
        # Load feature mapping
        if os.path.exists("feature_mapping.json"):
            with open("feature_mapping.json", "r") as f:
                feature_mapping = json.load(f)
                print(f"Loaded feature mapping with {len(feature_mapping)} features")
        
        # Load merged data if it exists
        if os.path.exists("merged_data.csv"):
            merged_data = pd.read_csv("merged_data.csv")
            insights_agent = CaseInsights(merged_data)
    else:
        print("Generating data and training model...")
        # Generate data
        clients, cases, case_notes = generate_synthetic_data()
        
        # Preprocess data
        merged_data, X_train, X_test, y_train, y_test = preprocess_data(clients, cases)
        
        # Train model
        model, feature_importance = train_evaluate_model(X_train, X_test, y_train, y_test)
        
        # Save the model and data for future use
        with open("case_model.pkl", "wb") as f:
            pickle.dump(model, f)
        
        merged_data.to_csv("merged_data.csv", index=False)
        
        # Initialize insights agent
        insights_agent = CaseInsights(merged_data)
        
        # Save feature names
        feature_mapping = {col: i for i, col in enumerate(X_train.columns)}
        with open("feature_mapping.json", "w") as f:
            json.dump(feature_mapping, f)

# Define API endpoints
@app.get("/")
async def root():
    return {"message": "Welcome to the Case Management AI API", "status": "online"}

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    global model, feature_mapping
    
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    try:
        # Load feature mapping if it exists but isn't loaded
        if not feature_mapping and os.path.exists("feature_mapping.json"):
            with open("feature_mapping.json", "r") as f:
                feature_mapping = json.load(f)
                
        if not feature_mapping:
            raise HTTPException(status_code=500, detail="Feature mapping not available")
            
        # Debug information
        print(f"Request data: {request.dict()}")
        
        # Get the model's expected feature count
        n_features = model.n_features_in_ if hasattr(model, 'n_features_in_') else 4
        print(f"Model expects {n_features} features")
        
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
        
        print(f"Input data shape: {input_data.shape}")
        
        # Make prediction
        prediction_prob = model.predict_proba(input_data)[0]
        prediction_class = model.predict(input_data)[0]
        
        # Return result with more detailed information
        result = {
            "prediction": "Resolved" if prediction_class == 1 else "Not Resolved",
            "probability": float(prediction_prob[1])  # Probability of being resolved
        }
        
        print(f"Prediction result: {result}")
        return result
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Prediction error: {str(e)}\n{error_details}")
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.post("/insights")
async def get_insights(request: InsightType):
    global insights_agent
    
    if insights_agent is None:
        raise HTTPException(status_code=500, detail="Insights agent not initialized")
    
    try:
        if request.insight_type == "common_case_types":
            return {"common_case_types": insights_agent.common_case_types().to_dict()}
        elif request.insight_type == "resolution_factors":
            return {"resolution_factors": insights_agent.resolution_factors().to_dict()}
        elif request.insight_type == "assignee_performance":
            # Convert DataFrame to dict for JSON serialization
            return {"assignee_performance": insights_agent.assignee_performance().to_dict(orient="index")}
        else:
            raise HTTPException(status_code=400, detail=f"Unknown insight type: {request.insight_type}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting insights: {str(e)}")

@app.get("/model-info")
async def model_info():
    global model
    
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    return {
        "model_type": str(type(model).__name__),
        "features": list(feature_mapping.keys()),
        "n_features": len(feature_mapping)
    }

# Run the app with uvicorn when this script is executed directly
if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=5000) 