from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import pickle
import os
from typing import List, Dict, Any, Optional
import json
import uvicorn
import numpy as np
from datetime import datetime, timedelta

# Import project modules (using relative imports)
from ..data.data_generator import generate_synthetic_data
from ..data.data_processor import preprocess_data
from ..model.model_trainer import train_evaluate_model
from .case_insights import CaseInsights

# Initialize FastAPI app
app = FastAPI(
    title="Case Management API",
    description="API for case management system with insights and predictions",
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
    
    try:
        print("Generating fresh synthetic data...")
        # Generate synthetic data
        clients, cases, case_notes = generate_synthetic_data(
            num_clients=100,  # Smaller sample for testing
            num_cases=500,
            num_notes=1000
        )
        
        # Store the data directly
        merged_data = cases
        
        # Initialize insights agent
        insights_agent = CaseInsights(merged_data)
        
        print(f"Generated {len(merged_data)} cases successfully")
        
    except Exception as e:
        print(f"Error during startup: {str(e)}")
        # Generate minimal test data
        merged_data = pd.DataFrame({
            'case_id': range(1, 11),
            'client_id': [1, 2, 3, 1, 2, 3, 1, 2, 3, 1],
            'case_type': ['Civil', 'Criminal', 'Family', 'Civil', 'Criminal', 'Family', 'Civil', 'Criminal', 'Family', 'Civil'],
            'status': ['Open', 'Closed', 'Open', 'Closed', 'Open', 'Closed', 'Open', 'Closed', 'Open', 'Closed'],
            'assignee': ['Agent1', 'Agent2', 'Agent1', 'Agent2', 'Agent1', 'Agent2', 'Agent1', 'Agent2', 'Agent1', 'Agent2'],
            'open_date': pd.date_range(start='2024-01-01', periods=10),
            'close_date': pd.date_range(start='2024-02-01', periods=10),
            'is_resolved': [True, False, True, False, True, False, True, False, True, False],
            'escalated': [False, True, False, True, False, True, False, True, False, True]
        })
        insights_agent = CaseInsights(merged_data)

# Define API endpoints
@app.get("/")
async def root():
    return {"message": "Welcome to the Case Management API", "status": "online"}

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    global model, feature_mapping
    
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    try:
        # Load feature mapping if it exists but isn't loaded
        if not feature_mapping and os.path.exists("config/feature_mapping.json"):
            with open("config/feature_mapping.json", "r") as f:
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

@app.get("/cases")
async def get_cases() -> List[Dict[str, Any]]:
    """Get all cases"""
    try:
        # Convert datetime columns to string format before serialization
        df = merged_data.copy()
        print(f"Initial columns: {df.columns.tolist()}")
        print(f"Data types: {df.dtypes}")
        
        # Convert datetime columns
        if 'open_date' in df.columns:
            df['open_date'] = pd.to_datetime(df['open_date']).dt.strftime('%Y-%m-%d')
        if 'close_date' in df.columns:
            df['close_date'] = pd.to_datetime(df['close_date']).dt.strftime('%Y-%m-%d')
        
        # Convert numeric columns to Python native types
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
        print(f"Numeric columns: {numeric_cols.tolist()}")
        for col in numeric_cols:
            df[col] = df[col].astype(float)
        
        # Convert boolean columns
        bool_cols = df.select_dtypes(include=['bool']).columns
        print(f"Boolean columns: {bool_cols.tolist()}")
        for col in bool_cols:
            df[col] = df[col].astype(bool)
        
        # Convert to records
        records = df.to_dict('records')
        print(f"Number of records: {len(records)}")
        
        # Ensure all values are JSON serializable
        for record in records:
            for key, value in record.items():
                if pd.isna(value):
                    record[key] = None
                elif isinstance(value, (np.int64, np.float64)):
                    record[key] = float(value)
        
        return records
    except Exception as e:
        import traceback
        print(f"Error in get_cases: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/metrics")
async def get_metrics() -> Dict[str, Any]:
    """Get case metrics"""
    total_cases = len(merged_data)
    active_cases = len(merged_data[merged_data["status"] == "Open"])
    resolved_cases = len(merged_data[merged_data["status"] == "Resolved"])
    
    # Calculate average resolution time for resolved cases
    resolved_df = merged_data[merged_data["status"] == "Resolved"].copy()
    resolved_df['resolution_time'] = (pd.to_datetime(resolved_df['close_date']) - 
                                    pd.to_datetime(resolved_df['open_date'])).dt.days
    avg_resolution_time = resolved_df['resolution_time'].mean()
    
    # Calculate escalation rate
    escalation_rate = len(merged_data[merged_data["escalated"] == True]) / total_cases
    
    return {
        "total_cases": total_cases,
        "active_cases": active_cases,
        "resolved_cases": resolved_cases,
        "avg_resolution_time": round(float(avg_resolution_time), 1),
        "escalation_rate": round(float(escalation_rate), 2)
    }

@app.get("/insights")
async def get_insights() -> Dict[str, List[str]]:
    """Get insights about cases"""
    insights = []
    
    # Most common case type
    case_type_counts = merged_data['case_type'].value_counts()
    most_common_type = case_type_counts.index[0]
    type_percentage = (case_type_counts[most_common_type] / len(merged_data)) * 100
    insights.append(f"Most common case type is {most_common_type} ({type_percentage:.1f}%)")
    
    # Assignee workload
    assignee_counts = merged_data['assignee'].value_counts()
    busiest_assignee = assignee_counts.index[0]
    insights.append(f"{busiest_assignee} has the highest case load ({assignee_counts[busiest_assignee]} cases)")
    
    # Escalation rate
    escalation_rate = (len(merged_data[merged_data["escalated"] == True]) / len(merged_data)) * 100
    insights.append(f"Escalation rate is {escalation_rate:.1f}%")
    
    return {"insights": insights}

@app.get("/predict")
async def predict_case(case_type: str, complexity: str, client_age: int, 
                      client_income_level: str, days_open: int, escalated: bool):
    """Predict case outcome"""
    # Implementation remains the same
    pass

# Run the app with uvicorn when this script is executed directly
if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=5000) 