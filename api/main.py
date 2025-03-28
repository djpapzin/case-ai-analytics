from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
import random
from typing import List, Dict, Any, Optional
from collections import Counter

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://ai-powered-legal-case-management-system.streamlit.app",
        "http://localhost:8501",
        "*"  # For development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def generate_mock_data(num_cases: int = 100) -> List[Dict[str, Any]]:
    """Generate mock case data"""
    case_types = ["Civil", "Criminal", "Family", "Corporate", "Real Estate"]
    statuses = ["Open", "In Progress", "Resolved", "Closed"]
    assignees = ["John", "Sarah", "Michael", "Emily", "David"]
    
    now = datetime.now()
    cases = []
    
    for i in range(num_cases):
        open_date = now - timedelta(days=random.randint(1, 365))
        status = random.choice(statuses)
        close_date = None
        
        if status in ["Resolved", "Closed"]:
            close_date = open_date + timedelta(days=random.randint(5, 90))
        
        case = {
            "case_id": f"CASE-{i+1000}",
            "client_id": f"CLIENT-{random.randint(100, 999)}",
            "case_type": random.choice(case_types),
            "status": status,
            "assignee": random.choice(assignees),
            "open_date": open_date.isoformat(),
            "close_date": close_date.isoformat() if close_date else None,
            "escalated": random.choice([True, False])
        }
        cases.append(case)
    
    return cases

@app.get("/")
async def root():
    return {"message": "Welcome to the Case Management API"}

@app.get("/cases")
async def get_cases():
    try:
        cases = generate_mock_data()
        return cases
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/metrics")
async def get_metrics():
    try:
        cases = generate_mock_data()
        
        total_cases = len(cases)
        active_cases = sum(1 for case in cases if case["status"] == "Open")
        resolved_cases = sum(1 for case in cases if case["status"] in ["Resolved", "Closed"])
        escalated_cases = sum(1 for case in cases if case["escalated"])
        
        return {
            "total_cases": total_cases,
            "active_cases": active_cases,
            "resolved_cases": resolved_cases,
            "escalation_rate": round(escalated_cases / total_cases, 2)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/insights")
async def get_insights():
    try:
        cases = generate_mock_data()
        insights = []
        
        # Count case types
        case_types = [case["case_type"] for case in cases]
        type_counter = Counter(case_types)
        most_common_type = type_counter.most_common(1)[0]
        type_percentage = (most_common_type[1] / len(cases)) * 100
        insights.append(f"Most common case type is {most_common_type[0]} ({type_percentage:.1f}%)")
        
        # Count assignee workload
        assignees = [case["assignee"] for case in cases]
        assignee_counter = Counter(assignees)
        busiest_assignee = assignee_counter.most_common(1)[0]
        insights.append(f"{busiest_assignee[0]} has the highest case load ({busiest_assignee[1]} cases)")
        
        # Calculate escalation rate
        escalated_cases = sum(1 for case in cases if case["escalated"])
        escalation_rate = (escalated_cases / len(cases)) * 100
        insights.append(f"Escalation rate is {escalation_rate:.1f}%")
        
        return {"insights": insights}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 