# Data Preprocessing Verification Guide

This document outlines the preprocessing steps and verification procedures for the Case Management AI System's data pipeline.

## Data Pipeline Overview

### Input Data Schema
```python
{
    'case_id': int64,          # Unique identifier for each case
    'client_id': int64,        # Unique identifier for each client
    'case_type': str,          # Type/category of the legal case
    'open_date': datetime64,   # Date when case was opened
    'close_date': datetime64,  # Date when case was closed
    'resolution_days': float64, # Days taken to resolve the case
    'status': str,             # Current status of the case
    'complexity': str,         # Case complexity level
    'assignee': str,           # Case handler/assignee
    'escalated': bool,         # Whether case was escalated
    'is_resolved': int32       # Resolution status (0/1)
}
```

## Preprocessing Steps

### 1. Data Type Verification
```python
def verify_data_types(df):
    expected_types = {
        'case_id': 'int64',
        'client_id': 'int64',
        'case_type': 'object',
        'open_date': 'datetime64[ns]',
        'close_date': 'datetime64[ns]',
        'resolution_days': 'float64',
        'status': 'object',
        'complexity': 'object',
        'assignee': 'object',
        'escalated': 'bool',
        'is_resolved': 'int32'
    }
    for col, dtype in expected_types.items():
        assert df[col].dtype == dtype, f"Column {col} has incorrect dtype"
```

### 2. Column Classification
- **Numeric Columns**: `['case_id', 'client_id', 'resolution_days']`
- **Boolean Columns**: `['escalated']`
- **Categorical Columns**: `['case_type', 'status', 'complexity', 'assignee']`
- **DateTime Columns**: `['open_date', 'close_date']`
- **Target Variable**: `['is_resolved']`

### 3. Feature Processing

#### Numeric Features
```python
def process_numeric_features(df):
    # Scale numerical features
    numeric_cols = ['resolution_days']
    scaler = StandardScaler()
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
    
    # Verify scaling
    assert df[numeric_cols].mean().abs().max() < 1e-10
    assert abs(df[numeric_cols].std() - 1).max() < 1e-10
```

#### Categorical Features
```python
def process_categorical_features(df):
    # Encode categorical variables
    categorical_cols = ['case_type', 'status', 'complexity', 'assignee']
    for col in categorical_cols:
        df[col] = LabelEncoder().fit_transform(df[col])
        
    # Verify encoding
    for col in categorical_cols:
        assert df[col].dtype in ['int32', 'int64']
```

#### DateTime Features
```python
def process_datetime_features(df):
    # Extract temporal features
    df['month'] = df['open_date'].dt.month
    df['day_of_week'] = df['open_date'].dt.dayofweek
    df['is_weekend'] = df['day_of_week'].isin([5, 6])
    
    # Verify temporal features
    assert df['month'].between(1, 12).all()
    assert df['day_of_week'].between(0, 6).all()
```

## Verification Procedures

### 1. Data Integrity Checks
```python
def verify_data_integrity(df):
    # Check for duplicates
    assert df['case_id'].is_unique
    
    # Check for missing values
    assert df.isnull().sum().sum() == 0
    
    # Verify date logic
    assert (df['close_date'] >= df['open_date']).all()
    
    # Verify resolution days
    assert (df['resolution_days'] >= 0).all()
```

### 2. Feature Engineering Verification
```python
def verify_feature_engineering(df):
    # Verify one-hot encoding
    assert set(df.columns).issuperset(['month', 'day_of_week', 'is_weekend'])
    
    # Verify derived features
    assert df['is_weekend'].dtype == bool
```

### 3. Data Distribution Checks
```python
def verify_distributions(df):
    # Check numeric distributions
    for col in ['resolution_days']:
        stats = df[col].describe()
        assert stats['min'] >= 0
        assert stats['max'] < float('inf')
    
    # Check categorical distributions
    for col in ['case_type', 'complexity']:
        assert df[col].nunique() < len(df) / 10  # Reasonable cardinality
```

## Quality Assurance

### 1. Sample Size Verification
```python
def verify_sample_size(df):
    # Verify minimum sample size
    assert len(df) >= 500
    
    # Verify class balance
    resolved_ratio = df['is_resolved'].mean()
    assert 0.2 <= resolved_ratio <= 0.8  # Reasonable class balance
```

### 2. Feature Importance Analysis
```python
def analyze_feature_importance(df, model):
    # Calculate feature importance
    importances = model.feature_importances_
    
    # Verify key features have significant importance
    assert importances.max() > 0.1
    assert importances.min() >= 0
```

## Monitoring and Logging

### 1. Preprocessing Metrics
- Number of records processed
- Processing time
- Memory usage
- Error rates

### 2. Data Quality Metrics
- Missing value rates
- Outlier detection rates
- Feature correlation matrix
- Class distribution

### 3. Performance Monitoring
```python
def monitor_preprocessing_performance():
    metrics = {
        'processing_time': [],
        'memory_usage': [],
        'error_rate': [],
        'records_processed': []
    }
    return metrics
```

## Best Practices

1. **Version Control**
   - Track preprocessing code changes
   - Version preprocessing parameters
   - Document feature engineering decisions

2. **Error Handling**
   - Log preprocessing errors
   - Implement fallback strategies
   - Monitor error patterns

3. **Documentation**
   - Document preprocessing steps
   - Maintain feature definitions
   - Track preprocessing decisions

4. **Testing**
   - Unit tests for preprocessing functions
   - Integration tests for pipeline
   - Regression tests for changes 