import unittest
import pandas as pd
from unittest.mock import patch
from dashboard import fetch_cases, fetch_metrics, fetch_insights

class TestDashboardIntegration(unittest.TestCase):
    def setUp(self):
        """Set up test data"""
        self.mock_cases_data = pd.DataFrame({
            'case_id': [1, 2, 3],
            'client_id': [101, 102, 103],
            'case_type': ['Type A', 'Type B', 'Type A'],
            'status': ['Open', 'Closed', 'Closed'],
            'assignee': ['Agent1', 'Agent2', 'Agent1'],
            'open_date': pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-03']),
            'close_date': pd.to_datetime(['2024-02-01', '2024-02-02', None]),
            'is_resolved': [True, True, False],
            'escalated': [False, True, False]
        })
        
        self.mock_metrics = {
            'total_cases': 3,
            'active_cases': 1,
            'resolved_cases': 2,
            'avg_resolution_time': 31.0,
            'escalation_rate': 0.33
        }
        
        self.mock_insights = {
            'insights': [
                'Most common case type is Type A (66.7%)',
                'Agent1 has the highest case load (2 cases)',
                'Escalation rate is 33.3%'
            ]
        }

    @patch('dashboard.requests.get')
    def test_fetch_cases(self, mock_get):
        """Test cases fetching functionality"""
        mock_get.return_value.json.return_value = self.mock_cases_data.to_dict('records')
        mock_get.return_value.status_code = 200
        
        cases_df = fetch_cases()
        self.assertIsNotNone(cases_df)
        self.assertIsInstance(cases_df, pd.DataFrame)
        self.assertEqual(len(cases_df), 3)
        self.assertTrue('case_id' in cases_df.columns)

    @patch('dashboard.requests.get')
    def test_fetch_metrics(self, mock_get):
        """Test metrics fetching functionality"""
        mock_get.return_value.json.return_value = self.mock_metrics
        mock_get.return_value.status_code = 200
        
        metrics = fetch_metrics()
        self.assertIsNotNone(metrics)
        self.assertIsInstance(metrics, dict)
        self.assertTrue('total_cases' in metrics)
        self.assertTrue('active_cases' in metrics)

    @patch('dashboard.requests.get')
    def test_fetch_insights(self, mock_get):
        """Test insights fetching functionality"""
        mock_get.return_value.json.return_value = self.mock_insights
        mock_get.return_value.status_code = 200
        
        insights = fetch_insights()
        self.assertIsNotNone(insights)
        self.assertIsInstance(insights, dict)
        self.assertTrue('insights' in insights)
        self.assertTrue(len(insights['insights']) > 0)

    def test_data_filtering(self):
        """Test data filtering functionality"""
        filtered_df = self.mock_cases_data[
            (self.mock_cases_data['case_type'] == 'Type A') &
            (self.mock_cases_data['status'] == 'Open')
        ]
        self.assertEqual(len(filtered_df), 1)

    def test_metrics_consistency(self):
        """Test metrics calculation consistency"""
        active_cases = len(self.mock_cases_data[self.mock_cases_data['status'] == 'Open'])
        self.assertEqual(active_cases, self.mock_metrics['active_cases'])

    def test_insights_relevance(self):
        """Test insights relevance to data"""
        type_a_count = len(self.mock_cases_data[self.mock_cases_data['case_type'] == 'Type A'])
        self.assertEqual(type_a_count, 2)
        type_a_percentage = (type_a_count / len(self.mock_cases_data)) * 100
        self.assertAlmostEqual(type_a_percentage, 66.7, places=1)

    @patch('dashboard.requests.get')
    def test_error_handling(self, mock_get):
        """Test error handling for API failures"""
        mock_get.side_effect = Exception('API Error')
        cases_df = fetch_cases()
        self.assertIsNone(cases_df)

if __name__ == '__main__':
    unittest.main() 