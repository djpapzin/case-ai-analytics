import os
import pandas as pd
from data_generator import generate_synthetic_data
from data_processor import preprocess_data

def main():
    """Generate and save synthetic data tables."""
    print("Generating synthetic data...")
    
    # Generate synthetic data
    clients_df, cases_df, case_notes_df = generate_synthetic_data(
        num_clients=1000,
        num_cases=5000,
        num_notes=10000
    )
    
    # Create data directory if it doesn't exist
    data_dir = os.path.join(os.path.dirname(__file__), 'tables')
    os.makedirs(data_dir, exist_ok=True)
    
    # Save raw tables
    print("\nSaving raw tables...")
    clients_df.to_csv(os.path.join(data_dir, 'clients.csv'), index=False)
    cases_df.to_csv(os.path.join(data_dir, 'cases.csv'), index=False)
    case_notes_df.to_csv(os.path.join(data_dir, 'case_notes.csv'), index=False)
    
    print("\nProcessing data for model...")
    # Process data for model
    merged_df, X_train, X_test, y_train, y_test = preprocess_data(clients_df, cases_df)
    
    # Save processed data
    print("\nSaving processed data...")
    merged_df.to_csv(os.path.join(data_dir, 'merged_data.csv'), index=False)
    X_train.to_csv(os.path.join(data_dir, 'X_train.csv'), index=False)
    X_test.to_csv(os.path.join(data_dir, 'X_test.csv'), index=False)
    y_train.to_csv(os.path.join(data_dir, 'y_train.csv'), index=False)
    y_test.to_csv(os.path.join(data_dir, 'y_test.csv'), index=False)
    
    # Print data info
    print("\nData Generation Complete!")
    print(f"Generated {len(clients_df)} clients")
    print(f"Generated {len(cases_df)} cases")
    print(f"Generated {len(case_notes_df)} case notes")
    print(f"\nTraining data shape: {X_train.shape}")
    print(f"Testing data shape: {X_test.shape}")
    
    # Print sample of each table
    print("\nSample of Clients table:")
    print(clients_df.head())
    print("\nSample of Cases table:")
    print(cases_df.head())
    print("\nSample of Case Notes table:")
    print(case_notes_df.head())

if __name__ == "__main__":
    main() 