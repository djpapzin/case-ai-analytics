"""
Case AI Analytics - Main Application Entry Point

This script serves as the entry point for the Case AI Analytics application.
It provides options to run different parts of the application:
1. Generate synthetic data
2. Train the model
3. Run the API server
4. Run analysis and generate insights

Usage:
    python app.py

The script will detect available command line arguments and run the appropriate functions.
"""

import os
import sys
import argparse
import uvicorn

def main():
    """Main entry point for the application"""
    parser = argparse.ArgumentParser(description='Case AI Analytics Application')
    parser.add_argument('--generate-data', action='store_true', help='Generate synthetic data')
    parser.add_argument('--train-model', action='store_true', help='Train the prediction model')
    parser.add_argument('--run-server', action='store_true', help='Run the API server')
    parser.add_argument('--run-analysis', action='store_true', help='Run analysis and generate insights')
    parser.add_argument('--port', type=int, default=8000, help='Port for the API server (default: 8000)')
    
    args = parser.parse_args()
    
    # If no arguments are provided, run the server by default
    if not any(vars(args).values()):
        print("No arguments provided, running API server on port 8000...")
        run_server(8000)
        return
    
    if args.generate_data:
        from src.data.data_generator import generate_synthetic_data
        print("Generating synthetic data...")
        clients, cases, case_notes = generate_synthetic_data()
        print("Data generation complete!")
        
    if args.train_model:
        from src.data.data_generator import generate_synthetic_data
        from src.data.data_processor import preprocess_data
        from src.model.model_trainer import train_evaluate_model
        
        print("Training model...")
        # First check if data exists, if not generate it
        if not os.path.exists("src/data/merged_data.csv"):
            print("Data not found, generating synthetic data first...")
            clients, cases, case_notes = generate_synthetic_data()
        
        # Preprocess data
        print("Preprocessing data...")
        merged_data, X_train, X_test, y_train, y_test = preprocess_data(clients, cases)
        
        # Train model
        print("Training model...")
        model, feature_importance = train_evaluate_model(X_train, X_test, y_train, y_test)
        print("Model training complete!")
        
    if args.run_server:
        run_server(args.port)
        
    if args.run_analysis:
        from src.api.case_insights import CaseInsights
        import pandas as pd
        
        print("Running analysis...")
        # Check if data exists
        if os.path.exists("src/data/merged_data.csv"):
            merged_data = pd.read_csv("src/data/merged_data.csv")
            insights = CaseInsights(merged_data)
            
            print("\nMost common case types:")
            print(insights.common_case_types())
            
            print("\nTop factors influencing resolution time:")
            print(insights.resolution_factors())
            
            print("\nAssignee performance summary:")
            print(insights.assignee_performance().head())
        else:
            print("Error: Data not found. Run with --generate-data first.")
            sys.exit(1)

def run_server(port=8000):
    """Run the API server"""
    print(f"Starting API server on port {port}...")
    uvicorn.run("src.api.api:app", host="0.0.0.0", port=port)

if __name__ == "__main__":
    main() 