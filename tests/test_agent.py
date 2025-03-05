import unittest
import pandas as pd
import numpy as np
from pathlib import Path
import sys
import os
import json
from datetime import datetime, timedelta

# Add src to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agent.case_insights import CaseInsightsAgent
from src.data.data_generator import generate_synthetic_data

class TestCaseInsightsAgent(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test data and agent once for all tests."""
        print("\nGenerating test data...")
        
        # Generate client data
        cls.clients = pd.DataFrame({
            'client_id': range(1, 201),
            'name': [f"Client_{i}" for i in range(1, 201)],
            'age': np.random.randint(18, 80, 200),
            'location': np.random.choice(['Urban', 'Suburban', 'Rural'], 200),
            'income_level': np.random.choice(['Low', 'Medium', 'High'], 200),
            'join_date': [
                datetime.now() - timedelta(days=np.random.randint(1, 1000))
                for _ in range(200)
            ]
        })
        
        # Generate case data
        case_types = [
            'Criminal Defense', 'Family Law', 'Civil Litigation',
            'Corporate', 'Intellectual Property', 'Estate Planning'
        ]
        assignees = [f"Attorney_{i}" for i in range(1, 6)]
        
        # Generate open dates
        open_dates = [
            datetime.now() - timedelta(days=np.random.randint(1, 365))
            for _ in range(1000)
        ]
        
        # Generate status with more closed cases
        status = np.random.choice(
            ['Closed', 'Open', 'Pending'],
            1000,
            p=[0.6, 0.3, 0.1]  # 60% closed, 30% open, 10% pending
        )
        
        cls.cases = pd.DataFrame({
            'case_id': range(1, 1001),
            'client_id': np.random.choice(cls.clients['client_id'], 1000),
            'case_type': np.random.choice(case_types, 1000),
            'assignee': np.random.choice(assignees, 1000),
            'open_date': open_dates,
            'status': status,
            'complexity_score': np.random.uniform(1, 10, 1000),
            'escalated': np.random.choice([True, False], 1000, p=[0.2, 0.8])
        })
        
        # Add close dates for closed cases
        cls.cases['close_date'] = cls.cases.apply(
            lambda x: x['open_date'] + timedelta(days=np.random.randint(1, 180))
            if x['status'] == 'Closed'
            else pd.NaT,
            axis=1
        )
        
        # Add derived features
        cls.cases['is_resolved'] = cls.cases['status'] == 'Closed'
        cls.cases['resolution_days'] = (cls.cases['close_date'] - cls.cases['open_date']).dt.days
        cls.cases.loc[cls.cases['resolution_days'].isna(), 'resolution_days'] = 0
        
        cls.cases['year_opened'] = cls.cases['open_date'].dt.year
        cls.cases['month_opened'] = cls.cases['open_date'].dt.month
        cls.cases['day_of_week_opened'] = cls.cases['open_date'].dt.dayofweek
        cls.cases['is_weekend'] = cls.cases['day_of_week_opened'].isin([5, 6])
        
        # Calculate case duration and complexity
        cls.cases['case_duration'] = np.where(
            cls.cases['status'] == 'Closed',
            cls.cases['resolution_days'],
            (datetime.now() - cls.cases['open_date']).dt.days
        )
        
        cls.cases['complexity'] = np.where(
            cls.cases['complexity_score'] >= 7, 'High',
            np.where(cls.cases['complexity_score'] >= 4, 'Medium', 'Low')
        )
        
        # Initialize agent
        cls.test_output_dir = "test_agent_output"
        cls.agent = CaseInsightsAgent(output_dir=cls.test_output_dir)
    
    def test_initialization(self):
        """Test agent initialization."""
        self.assertTrue(Path(self.test_output_dir).exists())
        self.assertEqual(self.agent.output_dir, Path(self.test_output_dir))
    
    def test_case_type_analysis(self):
        """Test case type analysis functionality."""
        results = self.agent.analyze_case_types(self.cases)
        
        # Check required keys
        required_keys = {'type_distribution', 'resolution_rates', 'visualization_path'}
        self.assertTrue(all(key in results for key in required_keys))
        
        # Check visualization
        self.assertTrue(Path(results['visualization_path']).exists())
        
        # Check distributions
        self.assertTrue(len(results['type_distribution']) > 0)
        self.assertTrue(all(0 <= rate <= 1 for rate in results['resolution_rates'].values()))
    
    def test_resolution_factors(self):
        """Test resolution factors analysis."""
        results = self.agent.analyze_resolution_factors(self.cases)
        
        # Check required keys
        required_keys = {'numerical_correlations', 'categorical_impact', 
                        'visualization_path'}
        self.assertTrue(all(key in results for key in required_keys))
        
        # Check visualization
        self.assertTrue(Path(results['visualization_path']).exists())
        
        # Check correlation values are in [-1, 1]
        correlations = list(results['numerical_correlations'].values())
        self.assertTrue(all(-1 <= c <= 1 for c in correlations))
    
    def test_assignee_performance(self):
        """Test assignee performance analysis."""
        results = self.agent.analyze_assignee_performance(self.cases)
        
        # Check required keys
        required_keys = {'assignee_metrics', 'visualization_path'}
        self.assertTrue(all(key in results for key in required_keys))
        
        # Check visualization
        self.assertTrue(Path(results['visualization_path']).exists())
        
        # Check metrics structure
        metrics = results['assignee_metrics']
        self.assertTrue(all(key in metrics for key in [
            'total_cases', 'resolution_rate', 'avg_resolution_days',
            'median_resolution_days', 'avg_complexity'
        ]))
    
    def test_escalation_patterns(self):
        """Test escalation patterns analysis."""
        results = self.agent.analyze_escalation_patterns(self.cases, self.clients)
        
        # Check required keys
        required_keys = {'demographic_patterns', 'visualization_path'}
        self.assertTrue(all(key in results for key in required_keys))
        
        # Check visualization
        self.assertTrue(Path(results['visualization_path']).exists())
        
        # Check demographic factors
        self.assertTrue(len(results['demographic_patterns']) > 0)
    
    def test_insights_report(self):
        """Test comprehensive insights report generation."""
        results = self.agent.generate_insights_report(self.cases, self.clients)
        
        # Check required sections
        required_sections = {
            'key_insights',
            'detailed_analysis',
            'visualizations'
        }
        self.assertTrue(all(section in results for section in required_sections))
        
        # Check key insights
        key_insights = results['key_insights']
        self.assertTrue(isinstance(key_insights['total_cases'], int))
        self.assertTrue(isinstance(key_insights['resolved_cases'], int))
        self.assertTrue(isinstance(key_insights['resolution_rate'], str))
        self.assertTrue(isinstance(key_insights['avg_resolution_time'], str))
        self.assertTrue(isinstance(key_insights['best_performing_assignee'], str))
        self.assertTrue(isinstance(key_insights['most_common_case_type'], str))
        
        # Check detailed analysis
        detailed_analysis = results['detailed_analysis']
        self.assertTrue('case_type_distribution' in detailed_analysis)
        self.assertTrue('resolution_factors' in detailed_analysis)
        self.assertTrue('assignee_performance' in detailed_analysis)
        self.assertTrue('escalation_patterns' in detailed_analysis)
        
        # Check visualizations
        visualizations = results['visualizations']
        self.assertTrue(all(key in visualizations for key in [
            'case_types', 'resolution_factors',
            'assignee_performance', 'escalation_patterns'
        ]))
        
        # Verify JSON serialization
        try:
            json.dumps(results)
        except Exception as e:
            self.fail(f"Insights report is not JSON serializable: {str(e)}")
    
    def test_edge_cases(self):
        """Test agent behavior with edge cases."""
        # Empty DataFrame
        empty_df = pd.DataFrame(columns=self.cases.columns)
        with self.assertRaises(ValueError):
            self.agent.analyze_case_types(empty_df)
        
        # Single case
        single_case = self.cases.iloc[[0]]
        results = self.agent.analyze_case_types(single_case)
        self.assertEqual(len(results['type_distribution']), 1)
        
        # Missing columns
        incomplete_df = self.cases.drop(columns=['assignee'])
        with self.assertRaises(KeyError):
            self.agent.analyze_assignee_performance(incomplete_df)

if __name__ == '__main__':
    unittest.main(verbosity=2) 