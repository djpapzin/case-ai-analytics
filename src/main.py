import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

from src.data.data_generator import generate_synthetic_data
from src.data.data_processor import preprocess_data
from src.model.model_trainer import train_evaluate_model
from src.api.case_insights import CaseInsights

def main():
    print("Step 1: Generating synthetic case management data...")
    clients, cases, case_notes = generate_synthetic_data()
    
    print("Step 2: Preprocessing data...")
    merged_data, X_train, X_test, y_train, y_test = preprocess_data(clients, cases)
    
    print("Step 3: Training and evaluating model...")
    model, feature_importance = train_evaluate_model(X_train, X_test, y_train, y_test)
    
    print("Step 4: Analyzing case insights...")
    insights = CaseInsights(merged_data)
    
    # Display some initial insights
    print("\nMost common case types:")
    print(insights.common_case_types())
    
    print("\nTop factors influencing resolution time:")
    print(insights.resolution_factors())
    
    print("\nAssignee performance summary:")
    print(insights.assignee_performance().head())
    
if __name__ == "__main__":
    main() 