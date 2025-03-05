import unittest
import numpy as np
import pandas as pd
from pathlib import Path
import sys
import os

# Add src to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.model.random_forest import RandomForestModel
from src.data.data_generator import generate_synthetic_data
from src.data.enhanced_processor import DataPreprocessor

class TestRandomForestModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test data and model once for all tests."""
        print("\nGenerating test data...")
        clients, cases, notes = generate_synthetic_data(200, 1000)  # Smaller dataset for testing
        
        # Preprocess data
        print("Preprocessing data...")
        preprocessor = DataPreprocessor()
        cls.df, cls.X_train, cls.X_test, cls.y_train, cls.y_test = preprocessor.preprocess(
            clients, cases, notes
        )
        
        # Train model
        print("Training model...")
        cls.model = RandomForestModel(n_estimators=50)  # Smaller model for testing
        cls.model.train(cls.X_train, cls.y_train)
        
        # Create test output directory
        cls.test_output_dir = Path("test_output")
        cls.test_output_dir.mkdir(exist_ok=True)
    
    def test_model_initialization(self):
        """Test model initialization with different parameters."""
        model = RandomForestModel(n_estimators=10, max_depth=5)
        self.assertEqual(model.model.n_estimators, 10)
        self.assertEqual(model.model.max_depth, 5)
    
    def test_model_training(self):
        """Test model training process."""
        # Check if feature names are stored
        self.assertIsNotNone(self.model.feature_names)
        self.assertEqual(len(self.model.feature_names), self.X_train.shape[1])
        
        # Check if model is trained
        self.assertTrue(hasattr(self.model.model, 'estimators_'))
    
    def test_model_prediction(self):
        """Test model prediction functionality."""
        # Make predictions
        predictions, probabilities = self.model.predict(self.X_test)
        
        # Check predictions shape and type
        self.assertEqual(len(predictions), len(self.X_test))
        self.assertTrue(all(isinstance(pred, (np.int64, int)) for pred in predictions))
        
        # Check probabilities shape
        self.assertEqual(probabilities.shape, (len(self.X_test), 2))  # Binary classification
        self.assertTrue(np.allclose(np.sum(probabilities, axis=1), 1))  # Probabilities sum to 1
    
    def test_model_evaluation(self):
        """Test model evaluation metrics."""
        metrics = self.model.evaluate(self.X_test, self.y_test, 
                                    output_dir=self.test_output_dir)
        
        # Check if all metrics are computed
        required_metrics = {'accuracy', 'precision', 'recall', 'f1'}
        self.assertTrue(all(metric in metrics for metric in required_metrics))
        
        # Check if metrics are in valid range [0, 1]
        self.assertTrue(all(0 <= metrics[m] <= 1 for m in metrics))
        
        # Check if evaluation plots are generated
        self.assertTrue((self.test_output_dir / 'confusion_matrix.png').exists())
        self.assertTrue((self.test_output_dir / 'feature_importance.png').exists())
    
    def test_feature_importance(self):
        """Test feature importance analysis."""
        importance_df = self.model.analyze_feature_importance()
        
        # Check DataFrame structure
        self.assertEqual(set(importance_df.columns), {'feature', 'importance'})
        self.assertEqual(len(importance_df), len(self.model.feature_names))
        
        # Check if importance scores sum to approximately 1
        self.assertAlmostEqual(importance_df['importance'].sum(), 1.0, places=5)
        
        # Check if importance scores are sorted
        self.assertTrue(importance_df['importance'].is_monotonic_decreasing)
    
    def test_model_persistence(self):
        """Test model saving and loading."""
        model_path = self.test_output_dir / 'test_model.joblib'
        
        # Save model
        self.model.save_model(model_path)
        self.assertTrue(model_path.exists())
        
        # Load model
        loaded_model = RandomForestModel.load_model(model_path)
        
        # Check if feature names are preserved
        self.assertEqual(loaded_model.feature_names, self.model.feature_names)
        
        # Compare predictions
        orig_pred, _ = self.model.predict(self.X_test)
        loaded_pred, _ = loaded_model.predict(self.X_test)
        self.assertTrue(np.array_equal(orig_pred, loaded_pred))
    
    def test_edge_cases(self):
        """Test model behavior with edge cases."""
        # Test with single sample
        single_sample = self.X_test.iloc[[0]]
        pred, prob = self.model.predict(single_sample)
        self.assertEqual(len(pred), 1)
        self.assertEqual(prob.shape, (1, 2))
        
        # Test with empty feature importance before training
        untrained_model = RandomForestModel()
        with self.assertRaises(ValueError):
            untrained_model.analyze_feature_importance()

if __name__ == '__main__':
    unittest.main(verbosity=2) 