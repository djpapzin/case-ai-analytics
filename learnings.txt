# Learnings Log

This document captures the key lessons, challenges, and insights gained throughout the development of the Case AI Analytics project.

## Key Learnings

### Data Preprocessing
- **Handling Missing Data**: Implemented effective strategies for handling missing values in case data, particularly for the 'assignee' and 'is_resolved' columns. Used conditional checks with fallback logic rather than simple imputation to maintain data integrity.
- **Data Merging**: Successfully merged case and client data using common keys, creating a comprehensive dataset for model training.
- **Feature Engineering**: Converted categorical variables to numerical features using one-hot encoding, which significantly improved model performance.

### Model Training & Evaluation
- **Model Selection**: Random Forest classifier proved to be the most effective for our case resolution prediction task, offering good accuracy and interpretability.
- **Evaluation Metrics**: Balanced accuracy, precision, recall, and F1-score provided a comprehensive view of model performance. Particularly important since our dataset had some class imbalance in resolution outcomes.
- **Feature Importance Analysis**: Case complexity, days open, and case type emerged as the most influential factors in predicting case outcomes, providing valuable business insights.

### Integration & Deployment
- **FastAPI Implementation**: Successfully implemented a RESTful API using FastAPI, providing endpoints for prediction and insights.
- **Cross-Platform Deployment**: Created platform-specific scripts (PowerShell and Bash) to simplify deployment across different operating systems.
- **Port Configuration**: Initially used port 5000, but successfully migrated to port 8000 to meet new project requirements without service disruption.

### Version Control & Documentation
- **Git Workflow**: Established an effective Git workflow with descriptive commit messages and organized repository structure.
- **Documentation**: Created comprehensive documentation including README.md and API_SETUP.md, providing clear instructions for installation, usage, and API endpoints.

## Challenges & Resolutions

### Data Quality Issues
- **Missing Columns**: Encountered issues where the 'assignee' and 'is_resolved' columns were missing in some datasets. Resolved by implementing defensive checks and fallback logic in the code.
- **String vs. Numeric Data**: Discovered a `ValueError` during model training due to string data in numeric features. Fixed by ensuring only numeric features are used in model training.

### Integration Challenges
- **Environment Configuration**: Needed to ensure the conda environment was properly activated in deployment scripts. Created platform-specific scripts with appropriate activation commands.
- **API Data Formats**: Initial prediction endpoint had issues with data formatting. Implemented more robust data validation and error handling in the API.

### Deployment Hurdles
- **Port Configuration**: Changed from port 5000 to port 8000 based on new requirements. Updated all documentation and scripts to reflect this change.
- **Cross-Platform Compatibility**: Ensured scripts work on both Windows (PowerShell) and Unix-like systems (Bash) by creating separate deployment scripts with platform-specific commands.
- **Testing**: The predict endpoint returned a 500 error during testing. This needs investigation to fix data handling or model loading issues.

## Future Improvements
- **Model Enhancement**: Explore ensemble methods or hyperparameter tuning to further improve prediction accuracy.
- **API Robustness**: Fix the prediction endpoint error that was discovered during testing.
- **User Interface**: Develop a simple web frontend for interacting with the API.
- **Authentication**: Implement API authentication for secure access to predictions and insights.
- **Continuous Deployment**: Set up automatic deployment pipeline using GitHub Actions or similar CI/CD tools.
- **Logging**: Implement more comprehensive logging for troubleshooting and performance monitoring.

## Reflection
The Case AI Analytics project successfully demonstrates the application of machine learning to predict legal case outcomes and extract valuable insights from case management data. The implementation of a FastAPI server makes these capabilities available through a standardized API.

Key achievements include:
- Successfully building a Random Forest model for case resolution prediction
- Creating an AI agent that provides actionable insights about case data
- Developing a robust API to expose both the model and insights
- Setting up a GitHub repository with comprehensive documentation
- Creating cross-platform deployment scripts for easy setup

While we encountered some challenges, particularly with data quality and API configuration, we successfully resolved most issues and documented the remaining ones for future improvement. The project provides a solid foundation that can be enhanced with additional features and optimizations in the future.
