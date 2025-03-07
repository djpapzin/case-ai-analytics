# Data Verification Guide

This document outlines the data verification process for the Case Management AI System.

## Data Schema

### Case Data
```python
{
    'case_id': int64,
    'client_id': int64,
    'case_type': object (string),
    'open_date': datetime64[ns],
    'close_date': datetime64[ns],
    'resolution_days': float64,
    'status': object (string),
    'complexity': object (string),
    'assignee': object (string),
    'escalated': bool,
    'is_resolved': int32
}
```

## Data Types

### Numeric Columns
- `case_id`
- `client_id`
- `resolution_days`

### Boolean Columns
- `escalated`

### Categorical Columns
- `case_type`
- `status`
- `complexity`
- `assignee`

### DateTime Columns
- `open_date`
- `close_date`

## Verification Steps

1. **Data Completeness**
   - Check for missing values
   - Verify required fields are present
   - Ensure date fields are properly formatted

2. **Data Consistency**
   - Validate relationships between fields
   - Check for logical consistency (e.g., close_date > open_date)
   - Verify status matches is_resolved flag

3. **Data Quality**
   - Check for outliers in numerical fields
   - Verify categorical values are within expected ranges
   - Validate date ranges are reasonable

## Automated Checks

The system performs the following automated verifications:

1. **Type Validation**
   ```python
   # Example of type checking
   assert isinstance(case_id, int)
   assert isinstance(escalated, bool)
   ```

2. **Range Validation**
   ```python
   # Example of range checking
   assert resolution_days >= 0
   assert case_id > 0
   ```

3. **Consistency Checks**
   ```python
   # Example of consistency validation
   assert open_date <= close_date
   assert is_resolved in [0, 1]
   ```

## Data Quality Metrics

The system tracks the following metrics:
- Number of records: 500 (current sample size)
- Missing value rate
- Outlier detection rate
- Data type consistency
- Field completion rate

## Verification Tools

1. **Data Summary**
   ```bash
   python tools/data_summary.py
   ```
   Provides overview of data statistics and quality metrics

2. **Schema Validation**
   ```bash
   python tools/validate_schema.py
   ```
   Verifies data against expected schema

3. **Consistency Check**
   ```bash
   python tools/check_consistency.py
   ```
   Runs logical consistency checks on the data

## Error Handling

Common data validation errors and their resolutions:

1. **Missing Values**
   - Log error details
   - Apply appropriate imputation strategy
   - Flag record for review

2. **Type Mismatches**
   - Convert to correct type if possible
   - Log conversion failures
   - Flag invalid records

3. **Consistency Violations**
   - Log inconsistent records
   - Apply business rules for resolution
   - Flag for manual review if needed

## Reporting

Data verification reports are generated in:
- `logs/data_validation.log`
- `reports/data_quality_report.html`
- `reports/validation_summary.csv`

## Best Practices

1. **Regular Validation**
   - Run verification daily
   - Monitor trends in data quality
   - Review error logs regularly

2. **Data Cleaning**
   - Document all cleaning steps
   - Maintain original data copies
   - Version control cleaned datasets

3. **Quality Monitoring**
   - Track quality metrics over time
   - Set alerts for quality degradation
   - Regular review of validation reports 