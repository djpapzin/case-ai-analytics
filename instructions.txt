# Instructions for AI Automation Developer Assessment

## Project Overview
The goal of this assessment is to build a machine learning model and an AI agent in Python using case management system data. The project is divided into two main parts:

### Part A: Machine Learning Model
- **Objective:** Predict case outcomes (e.g., resolved, pending, escalated) based on the data.
- **Dataset Requirements:**
  - Use at least three related tables (e.g., Cases, Clients, etc.).
  - Generate synthetic data if a real dataset is unavailable.
- **Key Tasks:**
  - Preprocess data: merge tables, handle missing values, normalize/scale features, and encode categorical variables.
  - Train a predictive model (e.g., decision tree).
  - Evaluate performance using accuracy, precision, recall, and F1-score.
  - Analyze feature importance to identify key predictors.
- **Bonus Objectives:**
  - Implement a time-based train-test split.
  - Deploy the model as an API using Flask or FastAPI.

### Part B: AI Agent for Case Insights
- **Objective:** Create an AI-powered assistant that provides actionable insights from the case management data.
- **Key Tasks:**
  - Analyze data to extract summary statistics and trends.
  - Use NLP techniques to process text from case descriptions and notes.
  - Develop functions or a class to answer questions such as:
    - What are the most common case types?
    - Which factors most influence case resolution time?
    - Which assignees have the highest resolution rates?
    - Are there discernible patterns in case escalations?
- **Bonus Objective:**
  - Build a chatbot interface using tools like LangChain or OpenAI’s API to allow natural language queries.

## Submission Requirements
- Combine all code and documentation into a single file or Jupyter Notebook.
- Include a README or Markdown file that explains:
  - The overall approach and design choices.
  - Detailed steps taken in data preparation, model training, and AI agent development.
  - Any challenges encountered and solutions implemented.
- Ensure code is clean, modular, well-commented, and follows best practices.
