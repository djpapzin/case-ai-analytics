import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns

class TimeBasedSplitter:
    """
    Implements time-based train-test splitting with validation and visualization.
    """
    
    def __init__(self, train_ratio=0.8, min_train_size=0.1, min_test_size=0.1):
        """
        Initialize the splitter.
        
        Args:
            train_ratio: Proportion of data to use for training (default: 0.8)
            min_train_size: Minimum acceptable proportion for training set (default: 0.1)
            min_test_size: Minimum acceptable proportion for test set (default: 0.1)
        """
        self.train_ratio = train_ratio
        self.min_train_size = min_train_size
        self.min_test_size = min_test_size
        self.split_date = None
        self.train_dates = None
        self.test_dates = None
    
    def validate_dates(self, dates):
        """Validate date column."""
        if not isinstance(dates, pd.Series):
            dates = pd.Series(dates)
        
        try:
            dates = pd.to_datetime(dates)
            return dates
        except Exception as e:
            raise ValueError(f"Invalid date format: {str(e)}")
    
    def analyze_time_distribution(self, dates):
        """Analyze the distribution of dates."""
        dates = self.validate_dates(dates)
        
        stats = {
            'min_date': dates.min(),
            'max_date': dates.max(),
            'date_range_days': (dates.max() - dates.min()).days,
            'total_records': len(dates),
            'unique_dates': dates.nunique(),
            'records_per_day': len(dates) / dates.nunique() if dates.nunique() > 0 else 0
        }
        
        return stats
    
    def split(self, df, date_column='open_date', validate=True):
        """
        Perform time-based split.
        
        Args:
            df: DataFrame to split
            date_column: Name of the date column to use for splitting
            validate: Whether to validate the split
            
        Returns:
            train_df, test_df: Split DataFrames
        """
        if date_column not in df.columns:
            raise ValueError(f"Date column '{date_column}' not found in DataFrame")
        
        # Convert dates
        dates = self.validate_dates(df[date_column])
        df = df.copy()
        df[date_column] = dates
        
        # Analyze distribution
        stats = self.analyze_time_distribution(dates)
        print("\nTime Distribution Analysis:")
        print("==========================")
        print(f"Date Range: {stats['min_date'].date()} to {stats['max_date'].date()}")
        print(f"Total Duration: {stats['date_range_days']} days")
        print(f"Total Records: {stats['total_records']}")
        print(f"Unique Dates: {stats['unique_dates']}")
        print(f"Average Records per Day: {stats['records_per_day']:.2f}")
        
        # Calculate split date
        self.split_date = dates.quantile(self.train_ratio)
        
        # Perform split
        train_df = df[df[date_column] < self.split_date]
        test_df = df[df[date_column] >= self.split_date]
        
        # Store date ranges
        self.train_dates = train_df[date_column]
        self.test_dates = test_df[date_column]
        
        # Validate split
        if validate:
            self.validate_split(train_df, test_df)
        
        return train_df, test_df
    
    def validate_split(self, train_df, test_df):
        """Validate the split meets requirements."""
        total_size = len(train_df) + len(test_df)
        train_ratio = len(train_df) / total_size
        test_ratio = len(test_df) / total_size
        
        print("\nSplit Validation:")
        print("================")
        print(f"Training Set: {len(train_df)} records ({train_ratio:.1%})")
        print(f"Testing Set: {len(test_df)} records ({test_ratio:.1%})")
        
        warnings = []
        if train_ratio < self.min_train_size:
            warnings.append(f"Training set too small: {train_ratio:.1%} < {self.min_train_size:.1%}")
        if test_ratio < self.min_test_size:
            warnings.append(f"Testing set too small: {test_ratio:.1%} < {self.min_test_size:.1%}")
        
        if warnings:
            print("\nWarnings:")
            for warning in warnings:
                print(f"- {warning}")
            return False
        
        print("\nValidation passed ✓")
        return True
    
    def plot_distribution(self, save_path=None):
        """Plot the distribution of dates in train and test sets."""
        if self.train_dates is None or self.test_dates is None:
            raise ValueError("No split has been performed yet")
        
        plt.figure(figsize=(12, 6))
        
        # Plot training dates
        plt.hist(self.train_dates, bins=50, alpha=0.5, label='Training Set', 
                color='blue', density=True)
        
        # Plot testing dates
        plt.hist(self.test_dates, bins=50, alpha=0.5, label='Testing Set', 
                color='red', density=True)
        
        plt.axvline(self.split_date, color='black', linestyle='--', 
                   label='Split Date')
        
        plt.title('Distribution of Dates in Train and Test Sets')
        plt.xlabel('Date')
        plt.ylabel('Density')
        plt.legend()
        
        if save_path:
            plt.savefig(save_path)
            plt.close()
        else:
            plt.show()

def demonstrate_split():
    """Demonstrate the time-based splitting with sample data."""
    from data_generator import generate_synthetic_data
    
    # Generate sample data
    print("Generating sample data...")
    clients, cases, _ = generate_synthetic_data(1000, 5000)
    
    # Create splitter
    splitter = TimeBasedSplitter(train_ratio=0.8, min_train_size=0.1, min_test_size=0.1)
    
    # Perform split
    print("\nPerforming time-based split...")
    train_df, test_df = splitter.split(cases, date_column='open_date')
    
    # Plot distribution
    print("\nGenerating distribution plot...")
    splitter.plot_distribution('time_split_distribution.png')
    
    print("\nSplit demonstration complete!")
    return train_df, test_df

if __name__ == "__main__":
    train_df, test_df = demonstrate_split() 