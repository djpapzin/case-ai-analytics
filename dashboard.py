import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import plotly.express as px
import random
import numpy as np
from src.agent.case_chatbot import CaseChatbot
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(
    page_title="Case Management Dashboard",
    page_icon="📊",
    layout="wide"
)

# Check for required environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# API configuration
# API_URL = "https://ai-automation-geyi53q75-djpapzins-projects.vercel.app"  # Production API URL
API_URL = "https://case-management-ai.onrender.com"  # Render.com deployment

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'chatbot' not in st.session_state:
    st.session_state.chatbot = CaseChatbot(api_url=API_URL)

# Mock data generation for when API is unavailable
def generate_mock_data(num_cases=100):
    """Generate mock data for testing"""
    case_types = ["Civil", "Criminal", "Family", "Corporate", "Real Estate"]
    statuses = ["Open", "In Progress", "Resolved", "Closed"]
    assignees = ["John", "Sarah", "Michael", "Emily", "David"]
    
    # Generate dates
    now = datetime.now()
    open_dates = [now - timedelta(days=random.randint(1, 365)) for _ in range(num_cases)]
    
    data = {
        "case_id": [f"CASE-{i+1000}" for i in range(num_cases)],
        "client_id": [f"CLIENT-{random.randint(100, 999)}" for _ in range(num_cases)],
        "case_type": [random.choice(case_types) for _ in range(num_cases)],
        "status": [random.choice(statuses) for _ in range(num_cases)],
        "assignee": [random.choice(assignees) for _ in range(num_cases)],
        "open_date": open_dates,
        "escalated": [random.choice([True, False]) for _ in range(num_cases)]
    }
    
    # Add close_date only for resolved and closed cases
    close_dates = []
    for i in range(num_cases):
        if data["status"][i] in ["Resolved", "Closed"]:
            close_date = data["open_date"][i] + timedelta(days=random.randint(5, 90))
            close_dates.append(close_date)
        else:
            close_dates.append(None)
    
    data["close_date"] = close_dates
    
    # Add is_resolved field
    data["is_resolved"] = [status in ["Resolved", "Closed"] for status in data["status"]]
    
    return pd.DataFrame(data)

def generate_mock_metrics(df):
    """Generate mock metrics based on dataframe"""
    total_cases = len(df)
    active_cases = len(df[df["status"] == "Open"])
    resolved_cases = len(df[df["is_resolved"] == True])
    
    # Calculate average resolution time for resolved cases
    resolved_df = df[df["is_resolved"] == True].copy()
    resolved_df["open_date"] = pd.to_datetime(resolved_df["open_date"])
    resolved_df["close_date"] = pd.to_datetime(resolved_df["close_date"])
    resolved_df["resolution_time"] = (resolved_df["close_date"] - resolved_df["open_date"]).dt.days
    avg_resolution_time = resolved_df["resolution_time"].mean()
    
    # Calculate escalation rate
    escalation_rate = len(df[df["escalated"] == True]) / total_cases
    
    return {
        "total_cases": total_cases,
        "active_cases": active_cases,
        "resolved_cases": resolved_cases,
        "avg_resolution_time": round(float(avg_resolution_time), 1),
        "escalation_rate": round(float(escalation_rate), 2)
    }

def generate_mock_insights(df):
    """Generate mock insights based on dataframe"""
    insights = []
    
    # Most common case type
    case_type_counts = df["case_type"].value_counts()
    most_common_type = case_type_counts.index[0]
    type_percentage = (case_type_counts[most_common_type] / len(df)) * 100
    insights.append(f"Most common case type is {most_common_type} ({type_percentage:.1f}%)")
    
    # Assignee workload
    assignee_counts = df["assignee"].value_counts()
    busiest_assignee = assignee_counts.index[0]
    insights.append(f"{busiest_assignee} has the highest case load ({assignee_counts[busiest_assignee]} cases)")
    
    # Escalation rate
    escalation_rate = (len(df[df["escalated"] == True]) / len(df)) * 100
    insights.append(f"Escalation rate is {escalation_rate:.1f}%")
    
    return {"insights": insights}

def fetch_data(endpoint: str, fallback_data: dict = None) -> dict:
    """Fetch data from API with graceful fallback to mock data."""
    try:
        response = requests.get(f"{API_URL}/{endpoint}", timeout=5)
        if response.status_code == 200:
            return response.json()
        raise Exception(f"API returned status code {response.status_code}")
    except Exception as e:
        st.warning(f"Using mock data for {endpoint} (API connection unavailable: {str(e)})")
        return fallback_data or generate_mock_data(endpoint)

def fetch_cases():
    """Fetch cases from the API or use mock data"""
    try:
        with st.spinner("Fetching case data..."):
            response = requests.get(f"{API_URL}/cases", timeout=5)
            if response.status_code == 200:
                data = response.json()
                df = pd.DataFrame(data)
                # Convert date columns to datetime
                if 'open_date' in df.columns:
                    df['open_date'] = pd.to_datetime(df['open_date'])
                if 'close_date' in df.columns:
                    df['close_date'] = pd.to_datetime(df['close_date'])
                return df
            else:
                st.warning(f"API returned status code: {response.status_code}. Using mock data instead.")
                return generate_mock_data()
    except Exception as e:
        st.warning(f"Could not connect to API: {str(e)}. Using mock data instead.")
        return generate_mock_data()

def fetch_metrics():
    """Fetch metrics from the API or calculate from mock data"""
    try:
        with st.spinner("Fetching metrics..."):
            response = requests.get(f"{API_URL}/metrics", timeout=5)
            if response.status_code == 200:
                return response.json()
            else:
                st.warning(f"API returned status code: {response.status_code}. Using calculated metrics instead.")
                cases_df = fetch_cases()
                return generate_mock_metrics(cases_df)
    except Exception as e:
        st.warning(f"Could not connect to API: {str(e)}. Using calculated metrics instead.")
        cases_df = fetch_cases()
        return generate_mock_metrics(cases_df)

def fetch_insights():
    """Fetch insights from the API or generate from mock data"""
    try:
        with st.spinner("Fetching insights..."):
            response = requests.get(f"{API_URL}/insights", timeout=5)
            if response.status_code == 200:
                return response.json()
            else:
                st.warning(f"API returned status code: {response.status_code}. Using generated insights instead.")
                cases_df = fetch_cases()
                return generate_mock_insights(cases_df)
    except Exception as e:
        st.warning(f"Could not connect to API: {str(e)}. Using generated insights instead.")
        cases_df = fetch_cases()
        return generate_mock_insights(cases_df)

def main():
    st.title("Case Management Dashboard")
    st.markdown("### AI-Powered Legal Case Management System")
    
    # Create tabs for dashboard and chat interface
    tab1, tab2 = st.tabs(["📊 Dashboard", "💬 AI Assistant"])
    
    with tab1:
        # Sidebar filters
        st.sidebar.header("Filters")
        
        # Fetch data
        cases_df = fetch_cases()
        
        if cases_df is not None:
            # Case type filter
            case_types = ["All"] + list(cases_df["case_type"].unique())
            selected_type = st.sidebar.selectbox("Case Type", case_types)
            
            # Status filter
            statuses = ["All"] + list(cases_df["status"].unique())
            selected_status = st.sidebar.selectbox("Status", statuses)
            
            # Date range filter
            min_date = pd.to_datetime(cases_df["open_date"]).min().date()
            max_date = pd.to_datetime(cases_df["open_date"]).max().date()
            date_range = st.sidebar.date_input(
                "Date Range",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date
            )
            
            # Apply filters
            filtered_df = cases_df.copy()
            if selected_type != "All":
                filtered_df = filtered_df[filtered_df["case_type"] == selected_type]
            if selected_status != "All":
                filtered_df = filtered_df[filtered_df["status"] == selected_status]
            if len(date_range) == 2:
                start_date, end_date = date_range
                filtered_df["open_date"] = pd.to_datetime(filtered_df["open_date"])
                filtered_df = filtered_df[
                    (filtered_df["open_date"].dt.date >= start_date) &
                    (filtered_df["open_date"].dt.date <= end_date)
                ]
            
            # Display metrics
            metrics = fetch_metrics()
            if metrics:
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Cases", metrics["total_cases"])
                with col2:
                    st.metric("Active Cases", metrics["active_cases"])
                with col3:
                    st.metric("Resolved Cases", metrics["resolved_cases"])
                with col4:
                    st.metric("Escalation Rate", f"{metrics['escalation_rate']:.1%}")
            
            # Display insights
            insights = fetch_insights()
            if insights:
                st.header("Key Insights")
                for insight in insights["insights"]:
                    st.info(insight)
            
            # Display case distribution
            st.header("Case Distribution")
            fig = px.pie(filtered_df, names="case_type", title="Cases by Type")
            st.plotly_chart(fig)
            
            # Display case timeline
            st.header("Case Timeline")
            filtered_df["open_date"] = pd.to_datetime(filtered_df["open_date"])
            filtered_df["close_date"] = pd.to_datetime(filtered_df["close_date"], errors='coerce')
            timeline_df = filtered_df.groupby(pd.Grouper(key="open_date", freq="ME")).size().reset_index(name="count")
            fig = px.line(timeline_df, x="open_date", y="count", title="Cases Over Time")
            st.plotly_chart(fig)
            
            # Display cases table
            st.header("Cases")
            st.dataframe(filtered_df)
            
            # Export functionality
            st.download_button(
                label="Export Data",
                data=filtered_df.to_csv(index=False),
                file_name="case_data.csv",
                mime="text/csv"
            )
        else:
            st.error("Unable to load case data. Please check the API connection.")
    
    with tab2:
        st.header("AI Case Assistant")
        
        # Check for API keys and display warning if missing
        if not GEMINI_API_KEY and not OPENAI_API_KEY:
            st.warning("""
            ⚠️ No API keys found. The chat functionality requires either:
            - A Gemini API key (recommended, free)
            - An OpenAI API key
            
            Please set the GEMINI_API_KEY or OPENAI_API_KEY environment variable in your Streamlit deployment settings.
            """)
        
        st.markdown("""
        Ask me anything about the cases! I can help you with:
        - Case trends and patterns
        - Performance metrics
        - Risk analysis
        - Recommendations
        """)
        
        # Chat interface
        user_input = st.chat_input("Ask a question about your cases...")
        
        # Display chat history
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Handle user input
        if user_input:
            # Display user message
            with st.chat_message("user"):
                st.markdown(user_input)
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            
            # Get and display assistant response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        response = st.session_state.chatbot.get_response_with_context(user_input)
                        st.markdown(response)
                        st.session_state.chat_history.append({"role": "assistant", "content": response})
                    except Exception as e:
                        error_msg = "An error occurred while processing your request. Please make sure your API keys are correctly set."
                        st.error(error_msg)
                        st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
        
        # Add a button to clear chat history
        if st.button("Clear Chat History"):
            st.session_state.chat_history = []
            st.session_state.chatbot.reset_conversation()
            st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("*Powered by DJ Papzin*")

if __name__ == "__main__":
    main() 