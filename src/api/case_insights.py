import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class CaseInsights:
    """
    AI agent for extracting insights from case management data.
    """
    
    def __init__(self, data):
        """
        Initialize the insights agent with case data.
        
        Args:
            data: DataFrame containing the merged case data
        """
        self.data = data
        self._preprocess()
        
    def _preprocess(self):
        """Prepare data for analysis."""
        # Convert dates to datetime if they aren't already
        date_columns = ['open_date', 'close_date']
        for col in date_columns:
            if col in self.data.columns:
                self.data[col] = pd.to_datetime(self.data[col])
        
        # Create a binary resolution indicator if needed
        if 'status' in self.data.columns and 'is_resolved' not in self.data.columns:
            self.data['is_resolved'] = np.where(self.data['status'] == 'Resolved', 1, 0)
    
    def common_case_types(self, top_n=5):
        """Return the most common case types."""
        if 'case_type' in self.data.columns:
            return self.data['case_type'].value_counts().head(top_n)
        else:
            # Look for encoded case type columns
            case_type_cols = [col for col in self.data.columns if col.startswith('case_type_')]
            if case_type_cols:
                case_counts = self.data[case_type_cols].sum().sort_values(ascending=False).head(top_n)
                return case_counts
            else:
                return "Case type information not found in the dataset."
    
    def resolution_factors(self, top_n=10):
        """Identify factors that contribute most to resolution time."""
        if 'resolution_days' not in self.data.columns:
            return "Resolution time information not found in the dataset."
        
        # Focus on resolved cases
        resolved_cases = self.data[self.data['resolution_days'].notna()]
        
        # Identify numerical columns for correlation analysis
        numerical_cols = resolved_cases.select_dtypes(include=['number']).columns
        numerical_cols = [col for col in numerical_cols 
                         if col not in ['case_id', 'client_id', 'resolution_days']]
        
        # Calculate correlation with resolution days
        correlations = resolved_cases[numerical_cols].corrwith(
            resolved_cases['resolution_days']).sort_values(ascending=False)
        
        return correlations.head(top_n)
    
    def assignee_performance(self):
        """Analyze performance metrics by assignee."""
        # Check for required columns
        target_column = None
        for col in ['is_resolved', 'status_Resolved']:
            if col in self.data.columns:
                target_column = col
                break
        
        if target_column is None:
            # Create a placeholder target if needed
            if 'status' in self.data.columns:
                self.data['is_resolved'] = self.data['status'].apply(
                    lambda x: 1 if x == 'Resolved' else 0)
                target_column = 'is_resolved'
            else:
                # No way to determine resolution, use a dummy column
                self.data['is_resolved'] = 1
                target_column = 'is_resolved'
        
        # Look for assignee column or encoded assignee columns
        if 'assignee' not in self.data.columns:
            # Look for encoded assignee columns
            assignee_cols = [col for col in self.data.columns if col.startswith('assignee_')]
            if assignee_cols:
                # Use the first assignee column for grouping
                main_assignee_col = assignee_cols[0]
                print(f"Using encoded assignee column: {main_assignee_col}")
                
                # Define columns to aggregate based on what's available
                agg_dict = {
                    target_column: 'mean',
                    'case_id': 'count'
                }
                
                if 'resolution_days' in self.data.columns:
                    agg_dict['resolution_days'] = 'mean'
                    
                if 'escalated' in self.data.columns:
                    agg_dict['escalated'] = 'mean'
                
                # Group by the assignee column
                metrics = self.data.groupby(main_assignee_col).agg(agg_dict)
                
                # Rename columns
                rename_dict = {
                    target_column: 'resolution_rate',
                    'case_id': 'case_count'
                }
                
                if 'resolution_days' in agg_dict:
                    rename_dict['resolution_days'] = 'avg_resolution_days'
                    
                if 'escalated' in agg_dict:
                    rename_dict['escalated'] = 'escalation_rate'
                    
                metrics = metrics.rename(columns=rename_dict)
                
                # Sort by resolution rate
                if 'resolution_rate' in metrics.columns:
                    metrics = metrics.sort_values('resolution_rate', ascending=False)
                
                return metrics
            else:
                # If no assignee columns at all, create a dummy summary
                print("No assignee information found. Returning summary statistics.")
                overall = {
                    'Overall': {
                        'case_count': len(self.data)
                    }
                }
                
                if target_column:
                    overall['Overall']['resolution_rate'] = self.data[target_column].mean()
                    
                if 'resolution_days' in self.data.columns:
                    overall['Overall']['avg_resolution_days'] = self.data['resolution_days'].mean()
                    
                if 'escalated' in self.data.columns:
                    overall['Overall']['escalation_rate'] = self.data['escalated'].mean()
                    
                return pd.DataFrame.from_dict(overall, orient='index')
        
        # If assignee column exists, use it directly
        # Define columns to aggregate based on what's available
        agg_dict = {
            target_column: 'mean',
            'case_id': 'count'
        }
        
        if 'resolution_days' in self.data.columns:
            agg_dict['resolution_days'] = 'mean'
            
        if 'escalated' in self.data.columns:
            agg_dict['escalated'] = 'mean'
        
        # Group by assignee and calculate metrics
        metrics = self.data.groupby('assignee').agg(agg_dict)
        
        # Rename columns
        rename_dict = {
            target_column: 'resolution_rate',
            'case_id': 'case_count'
        }
        
        if 'resolution_days' in agg_dict:
            rename_dict['resolution_days'] = 'avg_resolution_days'
            
        if 'escalated' in agg_dict:
            rename_dict['escalated'] = 'escalation_rate'
            
        metrics = metrics.rename(columns=rename_dict)
        
        # Sort by resolution rate
        if 'resolution_rate' in metrics.columns:
            metrics = metrics.sort_values('resolution_rate', ascending=False)
        
        return metrics
    
    def escalation_patterns(self):
        """Analyze patterns in case escalations."""
        if 'escalated' not in self.data.columns:
            return "Escalation information not found in the dataset."
        
        # Analyze escalation by case type
        escalation_by_type = pd.crosstab(
            self.data['case_type'], 
            self.data['escalated'],
            normalize='index'
        ).sort_values(True, ascending=False)
        
        # Analyze escalation by client demographics if available
        if 'age' in self.data.columns:
            # Create age groups
            self.data['age_group'] = pd.cut(
                self.data['age'], 
                bins=[0, 30, 45, 60, 100], 
                labels=['<30', '30-45', '45-60', '60+']
            )
            escalation_by_age = pd.crosstab(
                self.data['age_group'],
                self.data['escalated'],
                normalize='index'
            ).sort_values(True, ascending=False)
        else:
            escalation_by_age = "Age information not available"
        
        return {
            "by_case_type": escalation_by_type,
            "by_age_group": escalation_by_age
        }
    
    def plot_trends(self):
        """Plot case volume and resolution trends over time."""
        if 'open_date' not in self.data.columns:
            return "Date information not found in the dataset."
        
        # Create monthly time series
        self.data['month'] = self.data['open_date'].dt.to_period('M')
        monthly_cases = self.data.groupby('month').size()
        
        plt.figure(figsize=(12, 8))
        
        # Plot 1: Case volume over time
        plt.subplot(2, 1, 1)
        monthly_cases.plot(kind='line')
        plt.title('Case Volume Over Time')
        plt.ylabel('Number of Cases')
        
        # Plot 2: Resolution rates over time
        plt.subplot(2, 1, 2)
        self.data.groupby('month')['is_resolved'].mean().plot(kind='line')
        plt.title('Resolution Rate Over Time')
        plt.ylabel('Resolution Rate')
        
        plt.tight_layout()
        plt.savefig('case_trends.png')
        
        return "Plots saved to 'case_trends.png'"
    
    def get_insight(self, question):
        """
        Natural language interface to case insights.
        
        Args:
            question: String containing the question about case data
            
        Returns:
            String response with the requested insight
        """
        question = question.lower()
        
        if 'common' in question and ('case' in question or 'type' in question):
            return f"Most common case types:\n{self.common_case_types()}"
            
        elif 'resolution' in question and 'factor' in question:
            return f"Factors contributing to resolution time:\n{self.resolution_factors()}"
            
        elif 'assignee' in question or 'performance' in question:
            return f"Assignee performance:\n{self.assignee_performance()}"
            
        elif 'escalation' in question or 'escalated' in question:
            return f"Escalation patterns:\n{self.escalation_patterns()}"
            
        elif 'trend' in question or 'over time' in question:
            return self.plot_trends()
            
        else:
            return "I couldn't understand that question. Try asking about common case types, resolution factors, assignee performance, or escalation patterns."

    def analyze_data(self):
        """Analyze the case data and return insights"""
        total_cases = len(self.data)
        open_cases = len(self.data[self.data['status'] == 'Open'])
        escalated_cases = len(self.data[self.data['escalated'] == True])
        
        # Calculate case type distribution
        case_type_counts = self.data['case_type'].value_counts()
        most_common_type = case_type_counts.index[0]
        type_percentage = (case_type_counts[most_common_type] / total_cases) * 100
        
        # Calculate assignee workload
        assignee_counts = self.data['assignee'].value_counts()
        busiest_assignee = assignee_counts.index[0]
        assignee_cases = assignee_counts[busiest_assignee]
        
        # Calculate escalation rate
        escalation_rate = (escalated_cases / total_cases) * 100
        
        return {
            "total_cases": total_cases,
            "open_cases": open_cases,
            "escalated_cases": escalated_cases,
            "most_common_type": {
                "type": most_common_type,
                "percentage": type_percentage
            },
            "busiest_assignee": {
                "name": busiest_assignee,
                "cases": assignee_cases
            },
            "escalation_rate": escalation_rate
        }

if __name__ == "__main__":
    # Test insights
    from data_generator import generate_synthetic_data
    from data_processor import preprocess_data
    
    clients, cases, _ = generate_synthetic_data(100, 500)
    merged, _, _, _, _ = preprocess_data(clients, cases)
    
    insights = CaseInsights(merged)
    print(insights.common_case_types())
    print(insights.resolution_factors())
    print(insights.get_insight("What are the most common types of cases?")) 