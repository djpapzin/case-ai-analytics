import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, precision_score, recall_score, f1_score
import matplotlib.pyplot as plt

def train_evaluate_model(X_train, X_test, y_train, y_test):
    """
    Train a machine learning model and evaluate its performance.
    
    Args:
        X_train, X_test: Feature sets for training and testing
        y_train, y_test: Target variables for training and testing
        
    Returns:
        model: The trained model
        feature_importance: DataFrame containing feature importance
    """
    # Ensure we only use numeric columns
    print("Feature data types:")
    print(X_train.dtypes.value_counts())
    
    # Filter for numeric columns only
    numeric_columns = X_train.select_dtypes(include=['int64', 'float64']).columns
    if len(numeric_columns) == 0:
        raise ValueError("No numeric features found in the dataset")
    
    X_train_numeric = X_train[numeric_columns]
    X_test_numeric = X_test[numeric_columns]
    
    print(f"Using {len(numeric_columns)} numeric features for model training")
    print(f"Numeric features shape: {X_train_numeric.shape}")
    
    # Initialize the model (using RandomForest, which is more robust than a single decision tree)
    model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    
    # Train the model
    model.fit(X_train_numeric, y_train)
    
    # Make predictions
    y_pred = model.predict(X_test_numeric)
    
    # Evaluate the model
    print("\nModel Performance:")
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print(f"Precision: {precision_score(y_test, y_pred):.4f}")
    print(f"Recall: {recall_score(y_test, y_pred):.4f}")
    print(f"F1 Score: {f1_score(y_test, y_pred):.4f}")
    
    print("\nDetailed Classification Report:")
    print(classification_report(y_test, y_pred))
    
    # Extract feature importance
    feature_importance = pd.DataFrame({
        'feature': X_train_numeric.columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    # Plot feature importance
    plt.figure(figsize=(10, 6))
    top_n = min(15, len(feature_importance))
    plt.barh(feature_importance['feature'][:top_n], feature_importance['importance'][:top_n])
    plt.xlabel('Importance')
    plt.title(f'Top {top_n} Most Important Features')
    plt.tight_layout()
    plt.savefig('feature_importance.png')
    
    print("\nTop 10 most important features:")
    print(feature_importance.head(min(10, len(feature_importance))))
    
    return model, feature_importance

if __name__ == "__main__":
    # Test model training
    from data_generator import generate_synthetic_data
    from data_processor import preprocess_data
    
    clients, cases, _ = generate_synthetic_data(100, 500)
    merged, X_train, X_test, y_train, y_test = preprocess_data(clients, cases)
    model, importance = train_evaluate_model(X_train, X_test, y_train, y_test) 