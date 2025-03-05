import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer
from src.data.time_split import TimeBasedSplitter

class DataPreprocessor:
    """
    Comprehensive data preprocessor for case management data.
    Handles merging, cleaning, feature engineering, and preprocessing.
    """
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.numerical_imputer = SimpleImputer(strategy='median')
        self.categorical_imputer = SimpleImputer(strategy='most_frequent')
        
    def merge_tables(self, clients_df, cases_df, case_notes_df=None):
        """Merge all relevant tables."""
        # Start with cases and clients
        merged_df = pd.merge(cases_df, clients_df, on='client_id', how='left')
        
        if case_notes_df is not None:
            # Aggregate case notes information
            notes_agg = case_notes_df.groupby('case_id').agg({
                'note_id': 'count',
                'note_type': lambda x: x.value_counts().index[0],
                'note_text': lambda x: ' '.join(x),
                'created_by': 'nunique'
            }).rename(columns={
                'note_id': 'total_notes',
                'note_type': 'most_common_note_type',
                'note_text': 'combined_notes',
                'created_by': 'unique_creators'
            })
            
            # Merge with main dataframe
            merged_df = pd.merge(merged_df, notes_agg, on='case_id', how='left')
        
        return merged_df
    
    def handle_missing_values(self, df):
        """Handle missing values in the dataset."""
        # Identify numerical and categorical columns
        numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns
        categorical_cols = df.select_dtypes(include=['object']).columns
        
        # Handle missing values in numerical columns
        if len(numerical_cols) > 0:
            df[numerical_cols] = self.numerical_imputer.fit_transform(df[numerical_cols])
        
        # Handle missing values in categorical columns
        if len(categorical_cols) > 0:
            df[categorical_cols] = self.categorical_imputer.fit_transform(df[categorical_cols])
        
        return df
    
    def create_features(self, df):
        """Create new features from existing data."""
        # Convert date columns to datetime
        date_columns = ['open_date', 'close_date', 'join_date']
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col])
        
        # Time-based features
        if 'open_date' in df.columns:
            df['month_opened'] = df['open_date'].dt.month
            df['year_opened'] = df['open_date'].dt.year
            df['day_of_week_opened'] = df['open_date'].dt.dayofweek
            df['is_weekend'] = df['open_date'].dt.dayofweek.isin([5, 6]).astype(int)
        
        # Client tenure
        if 'join_date' in df.columns and 'open_date' in df.columns:
            df['client_tenure_days'] = (df['open_date'] - df['join_date']).dt.days
        
        # Case duration
        if 'close_date' in df.columns and 'open_date' in df.columns:
            df['case_duration'] = (df['close_date'] - df['open_date']).dt.days
        
        # Client age groups
        if 'age' in df.columns:
            df['age_group'] = pd.cut(df['age'], 
                                   bins=[0, 25, 35, 50, 65, 100],
                                   labels=['Young', 'Young Adult', 'Adult', 'Senior', 'Elderly'])
        
        # Case complexity score
        if 'complexity' in df.columns:
            complexity_map = {'Low': 1, 'Medium': 2, 'High': 3}
            df['complexity_score'] = df['complexity'].map(complexity_map)
        
        return df
    
    def encode_categorical(self, df):
        """Encode categorical variables."""
        # Identify categorical columns
        categorical_columns = ['case_type', 'status', 'complexity', 'assignee', 
                             'income_level', 'location', 'age_group']
        
        # One-hot encoding for categorical variables
        df_encoded = pd.get_dummies(df, 
                                  columns=[col for col in categorical_columns 
                                         if col in df.columns],
                                  drop_first=True)
        
        # Convert boolean to int
        boolean_columns = df_encoded.select_dtypes(include=['bool']).columns
        for col in boolean_columns:
            df_encoded[col] = df_encoded[col].astype(int)
        
        return df_encoded
    
    def normalize_numerical(self, df, columns=None):
        """Normalize numerical features."""
        if columns is None:
            columns = ['age', 'resolution_days', 'client_tenure_days', 
                      'case_duration', 'complexity_score']
        
        # Filter for columns that exist in the dataframe
        columns = [col for col in columns if col in df.columns]
        
        if len(columns) > 0:
            df[columns] = self.scaler.fit_transform(df[columns])
        
        return df
    
    def create_target(self, df):
        """Create the target variable."""
        if 'status' in df.columns:
            df['is_resolved'] = df['status'].apply(lambda x: 1 if x == 'Resolved' else 0)
        return df
    
    def split_data(self, df, target='is_resolved', test_size=0.2):
        """Split data into training and testing sets."""
        # Define features (exclude non-feature columns)
        exclude_cols = ['case_id', 'client_id', 'open_date', 'close_date', 
                       'join_date', 'status', target, 'combined_notes']
        features = [col for col in df.columns 
                   if col not in exclude_cols and not col.startswith('status_')]
        
        # Initialize time-based splitter
        splitter = TimeBasedSplitter(train_ratio=1-test_size, 
                                   min_train_size=0.1, 
                                   min_test_size=0.1)
        
        # Perform time-based split
        train_data, test_data = splitter.split(df, date_column='open_date')
        
        # Generate split visualization
        splitter.plot_distribution('data_split_distribution.png')
        
        X_train = train_data[features]
        y_train = train_data[target]
        X_test = test_data[features]
        y_test = test_data[target]
        
        return X_train, X_test, y_train, y_test
    
    def preprocess(self, clients_df, cases_df, case_notes_df=None):
        """Complete preprocessing pipeline."""
        print("Starting preprocessing pipeline...")
        
        # 1. Merge tables
        print("Merging tables...")
        df = self.merge_tables(clients_df, cases_df, case_notes_df)
        
        # 2. Handle missing values
        print("Handling missing values...")
        df = self.handle_missing_values(df)
        
        # 3. Create features
        print("Creating features...")
        df = self.create_features(df)
        
        # 4. Create target variable
        print("Creating target variable...")
        df = self.create_target(df)
        
        # 5. Identify and encode all categorical columns
        print("Encoding categorical variables...")
        categorical_columns = df.select_dtypes(include=['object', 'category']).columns
        df = pd.get_dummies(df, columns=categorical_columns, drop_first=True)
        
        # 6. Normalize numerical features
        print("Normalizing numerical features...")
        numerical_columns = df.select_dtypes(include=['int64', 'float64']).columns
        numerical_columns = [col for col in numerical_columns 
                            if col != 'is_resolved' and not col.startswith(tuple(categorical_columns))]
        if len(numerical_columns) > 0:
            df[numerical_columns] = self.scaler.fit_transform(df[numerical_columns])
        
        # 7. Split the data
        print("Splitting data...")
        X_train, X_test, y_train, y_test = self.split_data(df)
        
        print("Preprocessing complete!")
        print(f"Training data shape: {X_train.shape}")
        print(f"Testing data shape: {X_test.shape}")
        
        return df, X_train, X_test, y_train, y_test

if __name__ == "__main__":
    # Test the preprocessor
    from data_generator import generate_synthetic_data
    
    # Generate test data
    print("Generating test data...")
    clients, cases, notes = generate_synthetic_data(100, 500, 1000)
    
    # Initialize and run preprocessor
    preprocessor = DataPreprocessor()
    df, X_train, X_test, y_train, y_test = preprocessor.preprocess(clients, cases, notes)
    
    # Print summary
    print("\nPreprocessing Summary:")
    print("=====================")
    print(f"Total features: {X_train.shape[1]}")
    print("\nFeature list:")
    for col in X_train.columns:
        print(f"- {col}")
    print("\nTarget distribution:")
    print(y_train.value_counts(normalize=True)) 