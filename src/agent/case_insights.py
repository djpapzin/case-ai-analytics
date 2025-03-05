import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from datetime import datetime, timedelta

class CaseInsightsAgent:
    """
    AI agent for extracting insights from case management data.
    Provides analysis and visualization of case patterns, performance metrics,
    and business insights.
    """
    
    def __init__(self, output_dir: str = "insights_output"):
        """
        Initialize the insights agent.
        
        Args:
            output_dir: Directory to save visualization outputs
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def analyze_case_types(self, cases_df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze the distribution and patterns of case types.
        
        Args:
            cases_df: DataFrame containing case data
            
        Returns:
            Dictionary containing case type analysis results
        """
        if cases_df.empty:
            raise ValueError("Cannot analyze empty DataFrame")
        
        # Calculate case type distribution
        type_dist = cases_df['case_type'].value_counts()
        
        # Calculate resolution rate by case type
        resolution_by_type = cases_df.groupby('case_type')['status'].apply(
            lambda x: (x == 'Closed').mean()
        ).round(3)
        
        # Generate visualization
        plt.figure(figsize=(12, 6))
        sns.countplot(data=cases_df, x='case_type')
        plt.title('Distribution of Case Types')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(self.output_dir / 'case_types.png')
        plt.close()
        
        return {
            'type_distribution': type_dist.to_dict(),
            'resolution_rates': resolution_by_type.to_dict(),
            'visualization_path': str(self.output_dir / 'case_types.png')
        }
    
    def analyze_resolution_factors(self, cases_df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze factors contributing to case resolution time.
        
        Args:
            cases_df: DataFrame containing case data
            
        Returns:
            Dictionary containing resolution factor analysis
        """
        if cases_df.empty:
            raise ValueError("Cannot analyze empty DataFrame")
        
        # Calculate correlation between numerical features and resolution time
        numerical_cols = cases_df.select_dtypes(include=['int64', 'float64']).columns
        if 'case_duration' not in numerical_cols:
            raise KeyError("Required column 'case_duration' not found")
        
        correlations = cases_df[numerical_cols].corr()['case_duration'].sort_values(ascending=False)
        
        # Analyze categorical features' impact
        categorical_impact = {}
        for col in ['complexity', 'case_type', 'assignee']:
            if col in cases_df.columns:
                impact = cases_df.groupby(col)['case_duration'].agg([
                    'mean', 'median', 'count'
                ]).round(2)
                categorical_impact[col] = impact.to_dict()
        
        # Generate correlation plot
        plt.figure(figsize=(10, 6))
        sns.heatmap(
            cases_df[numerical_cols].corr()[['case_duration']].sort_values('case_duration', ascending=False),
            annot=True, cmap='coolwarm', center=0
        )
        plt.title('Correlation with Resolution Time')
        plt.tight_layout()
        plt.savefig(self.output_dir / 'resolution_factors.png')
        plt.close()
        
        return {
            'numerical_correlations': correlations.to_dict(),
            'categorical_impact': categorical_impact,
            'visualization_path': str(self.output_dir / 'resolution_factors.png')
        }
    
    def analyze_assignee_performance(self, cases_df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze performance metrics for case assignees.
        
        Args:
            cases_df: DataFrame containing case data
            
        Returns:
            Dictionary containing assignee performance metrics
        """
        if cases_df.empty:
            raise ValueError("Cannot analyze empty DataFrame")
        
        required_cols = ['assignee', 'case_id', 'is_resolved', 'resolution_days', 'complexity_score']
        missing_cols = [col for col in required_cols if col not in cases_df.columns]
        if missing_cols:
            raise KeyError(f"Missing required columns: {missing_cols}")
        
        # Calculate metrics per assignee
        assignee_metrics = cases_df.groupby('assignee').agg({
            'case_id': 'count',
            'is_resolved': 'mean',
            'resolution_days': ['mean', 'median'],
            'complexity_score': 'mean'
        }).round(3)
        
        # Rename columns for clarity
        assignee_metrics.columns = [
            'total_cases',
            'resolution_rate',
            'avg_resolution_days',
            'median_resolution_days',
            'avg_complexity'
        ]
        
        # Generate visualization
        plt.figure(figsize=(12, 6))
        sns.barplot(data=cases_df, x='assignee', y='resolution_days')
        plt.title('Average Resolution Time by Assignee')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(self.output_dir / 'assignee_performance.png')
        plt.close()
        
        return {
            'assignee_metrics': assignee_metrics.to_dict(),
            'visualization_path': str(self.output_dir / 'assignee_performance.png')
        }
    
    def analyze_escalation_patterns(
        self, cases_df: pd.DataFrame, clients_df: pd.DataFrame
    ) -> Dict[str, Any]:
        """
        Analyze patterns in case escalations related to client demographics.
        
        Args:
            cases_df: DataFrame containing case data
            clients_df: DataFrame containing client data
            
        Returns:
            Dictionary containing escalation pattern analysis
        """
        if cases_df.empty or clients_df.empty:
            raise ValueError("Cannot analyze empty DataFrame")
        
        required_cols = ['client_id', 'case_id', 'is_resolved']
        missing_cols = [col for col in required_cols if col not in cases_df.columns]
        if missing_cols:
            raise KeyError(f"Missing required columns in cases_df: {missing_cols}")
        
        # Merge case and client data
        merged_df = pd.merge(cases_df, clients_df, on='client_id', how='left')
        
        # Create age groups
        merged_df['age_group'] = pd.cut(
            merged_df['age'],
            bins=[0, 25, 35, 50, 65, 100],
            labels=['Young', 'Young Adult', 'Adult', 'Senior', 'Elderly']
        )
        
        # Analyze escalation rates by demographic factors
        demographic_factors = ['age_group', 'location', 'income_level']
        escalation_patterns = {}
        
        for factor in demographic_factors:
            if factor in merged_df.columns:
                pattern = merged_df.groupby(factor, observed=True).agg({
                    'case_id': 'count',
                    'is_resolved': ['mean', 'count']
                }).round(3)
                
                # Convert multi-level columns to string keys
                pattern.columns = [f"{col[0]}_{col[1]}" if isinstance(col, tuple) else col 
                                 for col in pattern.columns]
                
                # Convert to dictionary with string keys
                escalation_patterns[factor] = pattern.to_dict()
        
        # Generate visualization
        plt.figure(figsize=(12, 6))
        sns.boxplot(data=merged_df, x='age_group', y='case_duration')
        plt.title('Case Duration by Age Group')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(self.output_dir / 'escalation_patterns.png')
        plt.close()
        
        return {
            'demographic_patterns': escalation_patterns,
            'visualization_path': str(self.output_dir / 'escalation_patterns.png')
        }
    
    def generate_insights_report(
        self, cases_df: pd.DataFrame, clients_df: pd.DataFrame
    ) -> Dict[str, Any]:
        """
        Generate a comprehensive insights report from case and client data.
        
        Args:
            cases_df: DataFrame containing case data
            clients_df: DataFrame containing client data
            
        Returns:
            Dictionary containing various insights and analysis results
        """
        print("Analyzing case types...")
        case_type_analysis = self.analyze_case_types(cases_df)
        
        print("Analyzing resolution factors...")
        resolution_analysis = self.analyze_resolution_factors(cases_df)
        
        print("Analyzing assignee performance...")
        performance = self.analyze_assignee_performance(cases_df)
        
        print("Analyzing escalation patterns...")
        escalation_analysis = self.analyze_escalation_patterns(cases_df, clients_df)
        
        # Get the best performing assignee based on resolution rate
        assignee_metrics = pd.DataFrame(performance['assignee_metrics'])
        best_assignee = assignee_metrics['resolution_rate'].idxmax()
        
        # Calculate overall metrics
        total_cases = len(cases_df)
        resolved_cases = cases_df['status'].eq('Closed').sum()
        resolution_rate = (resolved_cases / total_cases) * 100
        avg_resolution_time = cases_df.loc[cases_df['status'] == 'Closed', 'resolution_days'].mean()
        
        return {
            'key_insights': {
                'total_cases': total_cases,
                'resolved_cases': int(resolved_cases),
                'resolution_rate': f"{resolution_rate:.1f}%",
                'avg_resolution_time': f"{avg_resolution_time:.1f} days",
                'best_performing_assignee': best_assignee,
                'most_common_case_type': max(case_type_analysis['type_distribution'].items(), 
                                        key=lambda x: x[1])[0]
            },
            'detailed_analysis': {
                'case_type_distribution': case_type_analysis['type_distribution'],
                'resolution_factors': resolution_analysis['numerical_correlations'],
                'assignee_performance': performance['assignee_metrics'],
                'escalation_patterns': escalation_analysis['demographic_patterns']
            },
            'visualizations': {
                'case_types': case_type_analysis['visualization_path'],
                'resolution_factors': resolution_analysis['visualization_path'],
                'assignee_performance': performance['visualization_path'],
                'escalation_patterns': escalation_analysis['visualization_path']
            }
        }

def generate_sample_data(num_clients=1000, num_cases=5000, num_notes=10000):
    """Generate sample data for demonstration purposes."""
    print("Generating sample data...")
    
    # Generate client data
    clients = pd.DataFrame({
        'client_id': range(1, num_clients + 1),
        'name': [f"Client_{i}" for i in range(1, num_clients + 1)],
        'age': np.random.randint(18, 80, num_clients),
        'location': np.random.choice(['Urban', 'Suburban', 'Rural'], num_clients),
        'income_level': np.random.choice(['Low', 'Medium', 'High'], num_clients),
        'join_date': [
            datetime.now() - timedelta(days=np.random.randint(1, 1000))
            for _ in range(num_clients)
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
        for _ in range(num_cases)
    ]
    
    # Generate status with more closed cases
    status = np.random.choice(
        ['Closed', 'Open', 'Pending'],
        num_cases,
        p=[0.6, 0.3, 0.1]  # 60% closed, 30% open, 10% pending
    )
    
    cases = pd.DataFrame({
        'case_id': range(1, num_cases + 1),
        'client_id': np.random.choice(clients['client_id'], num_cases),
        'case_type': np.random.choice(case_types, num_cases),
        'assignee': np.random.choice(assignees, num_cases),
        'open_date': open_dates,
        'status': status,
        'complexity_score': np.random.uniform(1, 10, num_cases),
        'escalated': np.random.choice([True, False], num_cases, p=[0.2, 0.8])
    })
    
    # Add close dates for closed cases (between 1 and 180 days after open date)
    cases['close_date'] = cases.apply(
        lambda x: x['open_date'] + timedelta(days=np.random.randint(1, 180))
        if x['status'] == 'Closed'
        else pd.NaT,
        axis=1
    )
    
    # Add derived features
    cases['is_resolved'] = cases['status'] == 'Closed'
    cases['resolution_days'] = (cases['close_date'] - cases['open_date']).dt.days
    cases.loc[cases['resolution_days'].isna(), 'resolution_days'] = 0
    
    cases['year_opened'] = cases['open_date'].dt.year
    cases['month_opened'] = cases['open_date'].dt.month
    cases['day_of_week_opened'] = cases['open_date'].dt.dayofweek
    cases['is_weekend'] = cases['day_of_week_opened'].isin([5, 6])
    
    # Calculate case duration and complexity
    cases['case_duration'] = np.where(
        cases['status'] == 'Closed',
        cases['resolution_days'],
        (datetime.now() - cases['open_date']).dt.days
    )
    
    cases['complexity'] = np.where(
        cases['complexity_score'] >= 7, 'High',
        np.where(cases['complexity_score'] >= 4, 'Medium', 'Low')
    )
    
    print(f"Generated {num_clients} clients, {num_cases} cases, and {num_notes} case notes")
    return clients, cases

def demonstrate_agent():
    """
    Demonstrate the AI agent's functionality with sample data.
    """
    # Generate sample data
    print("Generating sample data...")
    clients, cases = generate_sample_data(1000, 5000)
    
    print("\nAvailable columns in cases:")
    print("=========================")
    for col in sorted(cases.columns):
        print(f"- {col}")
    
    print("\nAvailable columns in clients:")
    print("==========================")
    for col in sorted(clients.columns):
        print(f"- {col}")
    
    # Initialize agent
    agent = CaseInsightsAgent(output_dir="agent_demo_output")
    
    # Generate insights report
    print("\nGenerating insights report...")
    insights = agent.generate_insights_report(cases, clients)
    
    # Display key insights
    print("\nKey Insights:")
    print("============")
    for key, value in insights['key_insights'].items():
        print(f"{key.replace('_', ' ').title()}: {value}")
    
    return agent, insights

if __name__ == "__main__":
    agent, insights = demonstrate_agent() 