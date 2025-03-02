from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import pickle
import os
from typing import List, Dict, Any, Optional
import json
import uvicorn

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
    global model, insights_agent, merged_data
    
    # Check if a saved model exists, otherwise generate and train
    if os.path.exists("case_model.pkl"):
        print("Loading existing model...")
        with open("case_model.pkl", "rb") as f:
            model = pickle.load(f)
        
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
        global feature_mapping
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
        # Convert request to features
        feature_vector = [0] * len(feature_mapping)
        
        # Map categorical values to one-hot encoding
        case_type_col = f"case_type_{request.case_type}"
        if case_type_col in feature_mapping:
            feature_vector[feature_mapping[case_type_col]] = 1
            
        complexity_col = f"complexity_{request.complexity}"
        if complexity_col in feature_mapping:
            feature_vector[feature_mapping[complexity_col]] = 1
            
        income_level_col = f"income_level_{request.client_income_level}"
        if income_level_col in feature_mapping:
            feature_vector[feature_mapping[income_level_col]] = 1
        
        # Set numerical values
        if "age" in feature_mapping:
            feature_vector[feature_mapping["age"]] = request.client_age
            
        if "days_open" in feature_mapping and request.days_open is not None:
            feature_vector[feature_mapping["days_open"]] = request.days_open
            
        if "escalated" in feature_mapping:
            feature_vector[feature_mapping["escalated"]] = 1 if request.escalated else 0
        
        # Make prediction
        prediction_prob = model.predict_proba([feature_vector])[0]
        prediction_class = model.predict([feature_vector])[0]
        
        # Return result
        return {
            "prediction": "Resolved" if prediction_class == 1 else "Not Resolved",
            "probability": float(prediction_prob[1])  # Probability of being resolved
        }
    except Exception as e:
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