from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

class RandomForestModel:
    """
    Random Forest model for case outcome prediction.
    Includes training, evaluation, feature importance analysis, and prediction capabilities.
    """
    
    def __init__(self, n_estimators=100, max_depth=None, random_state=42):
        """
        Initialize the model with specified parameters.
        
        Args:
            n_estimators: Number of trees in the forest
            max_depth: Maximum depth of the trees
            random_state: Random seed for reproducibility
        """
        self.model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=random_state
        )
        self.feature_names = None
        
    def train(self, X_train, y_train):
        """
        Train the model on the provided data.
        
        Args:
            X_train: Training features
            y_train: Training labels
        """
        self.feature_names = X_train.columns.tolist()
        self.model.fit(X_train, y_train)
        
    def predict(self, X):
        """
        Make predictions on new data.
        
        Args:
            X: Features to predict on
            
        Returns:
            Predictions and their probabilities
        """
        predictions = self.model.predict(X)
        probabilities = self.model.predict_proba(X)
        return predictions, probabilities
    
    def evaluate(self, X_test, y_test, output_dir=None):
        """
        Evaluate model performance and generate metrics.
        
        Args:
            X_test: Test features
            y_test: Test labels
            output_dir: Directory to save evaluation plots
            
        Returns:
            Dictionary of evaluation metrics
        """
        predictions = self.model.predict(X_test)
        
        # Calculate metrics
        metrics = {
            'accuracy': accuracy_score(y_test, predictions),
            'precision': precision_score(y_test, predictions, average='weighted'),
            'recall': recall_score(y_test, predictions, average='weighted'),
            'f1': f1_score(y_test, predictions, average='weighted')
        }
        
        # Generate confusion matrix
        cm = confusion_matrix(y_test, predictions)
        
        if output_dir:
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Plot confusion matrix
            plt.figure(figsize=(8, 6))
            sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
            plt.title('Confusion Matrix')
            plt.ylabel('True Label')
            plt.xlabel('Predicted Label')
            plt.savefig(output_dir / 'confusion_matrix.png')
            plt.close()
            
            # Plot feature importance
            self.plot_feature_importance(output_dir / 'feature_importance.png')
        
        return metrics
    
    def analyze_feature_importance(self):
        """
        Analyze and return feature importance scores.
        
        Returns:
            DataFrame with feature importance scores
        """
        if not self.feature_names:
            raise ValueError("Model hasn't been trained yet")
            
        importance_scores = self.model.feature_importances_
        feature_importance = pd.DataFrame({
            'feature': self.feature_names,
            'importance': importance_scores
        })
        return feature_importance.sort_values('importance', ascending=False)
    
    def plot_feature_importance(self, save_path=None):
        """
        Plot feature importance scores.
        
        Args:
            save_path: Path to save the plot
        """
        importance_df = self.analyze_feature_importance()
        
        plt.figure(figsize=(12, 6))
        sns.barplot(data=importance_df.head(15), x='importance', y='feature')
        plt.title('Top 15 Most Important Features')
        plt.xlabel('Importance Score')
        plt.ylabel('Feature')
        
        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
            plt.close()
        else:
            plt.show()
    
    def save_model(self, model_path):
        """
        Save the trained model to disk.
        
        Args:
            model_path: Path to save the model
        """
        model_data = {
            'model': self.model,
            'feature_names': self.feature_names
        }
        joblib.dump(model_data, model_path)
    
    @classmethod
    def load_model(cls, model_path):
        """
        Load a trained model from disk.
        
        Args:
            model_path: Path to the saved model
            
        Returns:
            Loaded RandomForestModel instance
        """
        model_data = joblib.load(model_path)
        instance = cls()
        instance.model = model_data['model']
        instance.feature_names = model_data['feature_names']
        return instance

def demonstrate_model():
    """
    Demonstrate the model's functionality with sample data.
    """
    from src.data.data_generator import generate_synthetic_data
    from src.data.enhanced_processor import DataPreprocessor
    
    # Generate and preprocess data
    print("Generating and preprocessing data...")
    clients, cases, notes = generate_synthetic_data(1000, 5000)
    
    preprocessor = DataPreprocessor()
    df, X_train, X_test, y_train, y_test = preprocessor.preprocess(clients, cases, notes)
    
    # Create and train model
    print("\nTraining model...")
    model = RandomForestModel(n_estimators=100)
    model.train(X_train, y_train)
    
    # Evaluate model
    print("\nEvaluating model...")
    metrics = model.evaluate(X_test, y_test, output_dir='model_evaluation')
    
    print("\nModel Performance:")
    for metric, value in metrics.items():
        print(f"{metric.capitalize()}: {value:.3f}")
    
    # Analyze feature importance
    print("\nTop 5 Most Important Features:")
    importance_df = model.analyze_feature_importance()
    print(importance_df.head())
    
    # Save model
    print("\nSaving model...")
    model.save_model('random_forest_model.joblib')
    
    return model, metrics

if __name__ == "__main__":
    model, metrics = demonstrate_model() 