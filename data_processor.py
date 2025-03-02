import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def preprocess_data(clients_df, cases_df):
    """
    Preprocess the data for model training.
    
    Args:
        clients_df: DataFrame with client information
        cases_df: DataFrame with case information
        
    Returns:
        merged_df: The merged dataset
        X_train, X_test, y_train, y_test: Train/test split for modeling
    """
    # Merge the datasets
    merged_df = pd.merge(cases_df, clients_df, on='client_id')
    
    # Convert dates to datetime if they aren't already
    date_columns = ['open_date', 'close_date', 'join_date']
    for col in date_columns:
        if col in merged_df.columns:
            merged_df[col] = pd.to_datetime(merged_df[col])
    
    # Feature engineering
    merged_df['client_tenure_days'] = (merged_df['open_date'] - 
                                      merged_df['join_date']).dt.days
    
    # Create time-based features
    merged_df['month_opened'] = merged_df['open_date'].dt.month
    merged_df['year_opened'] = merged_df['open_date'].dt.year
    merged_df['day_of_week_opened'] = merged_df['open_date'].dt.dayofweek
    
    # Handle missing values - using pandas Series method instead of deprecated chained assignment
    if 'resolution_days' in merged_df.columns:
        median_resolution = merged_df['resolution_days'].median()
        merged_df['resolution_days'] = merged_df['resolution_days'].fillna(median_resolution)
    
    # Encode categorical variables
    categorical_columns = ['case_type', 'status', 'complexity', 'assignee', 
                          'income_level', 'location']
    
    # Use pandas get_dummies for one-hot encoding
    merged_df = pd.get_dummies(merged_df, columns=[col for col in categorical_columns 
                                                 if col in merged_df.columns],
                              drop_first=True)
    
    # Convert boolean to int
    if 'escalated' in merged_df.columns:
        merged_df['escalated'] = merged_df['escalated'].astype(int)
    
    # Create binary target variable
    # Create a binary target (1 if resolved, 0 otherwise)
    if 'status' in merged_df.columns:
        merged_df['is_resolved'] = merged_df['status'].apply(
            lambda x: 1 if x == 'Resolved' else 0)
        target = 'is_resolved'
    elif 'status_Resolved' in merged_df.columns:
        target = 'status_Resolved'
    else:
        # If no status column, create a placeholder
        merged_df['is_resolved'] = 1
        target = 'is_resolved'
    
    # Define features - exclude certain columns and target-related columns
    features = [col for col in merged_df.columns 
                if col not in ['case_id', 'client_id', 'open_date', 'close_date', 'join_date', 'status', 'is_resolved'] 
                and not col.startswith('status_')]
    
    # Use regular train-test split if time-based split isn't feasible
    train_cutoff = pd.Timestamp('2022-07-01')
    train_data = merged_df[merged_df['open_date'] < train_cutoff]
    test_data = merged_df[merged_df['open_date'] >= train_cutoff]
    
    # If either train or test is empty, use regular split instead
    if len(train_data) < 10 or len(test_data) < 10:
        print("Time-based split resulted in insufficient data. Using random split instead.")
        train_data, test_data = train_test_split(merged_df, test_size=0.2, random_state=42)
    
    X_train = train_data[features]
    y_train = train_data[target]
    X_test = test_data[features]
    y_test = test_data[target]
    
    # Scale numerical features
    scaler = StandardScaler()
    numerical_cols = [col for col in ['age', 'resolution_days', 'client_tenure_days'] 
                      if col in X_train.columns]
    
    if len(numerical_cols) > 0 and len(X_train) > 0:
        X_train[numerical_cols] = scaler.fit_transform(X_train[numerical_cols])
        if len(X_test) > 0:
            X_test[numerical_cols] = scaler.transform(X_test[numerical_cols])
    
    print(f"Training data shape: {X_train.shape}, Test data shape: {X_test.shape}")
    
    return merged_df, X_train, X_test, y_train, y_test

if __name__ == "__main__":
    # Test preprocessing
    from data_generator import generate_synthetic_data
    clients, cases, _ = generate_synthetic_data(100, 500)
    merged, X_train, X_test, y_train, y_test = preprocess_data(clients, cases)
    print("Features:", X_train.columns.tolist())
    print("Target distribution:", y_train.value_counts()) 