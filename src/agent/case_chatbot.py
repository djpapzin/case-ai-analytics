from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv
import pandas as pd
import requests

# Load environment variables
load_dotenv()

class CaseChatbot:
    def __init__(self, api_url="http://localhost:8000"):
        """Initialize the chatbot with API connection and LangChain components."""
        self.api_url = api_url
        
        # Initialize chat model (Gemini by default, fallback to OpenAI)
        self.chat = self._initialize_chat_model()
        
        # Create conversation memory
        self.memory = ConversationBufferMemory()
        
        # Define the conversation prompt
        self.prompt = PromptTemplate(
            input_variables=["history", "input"],
            template="""You are an AI assistant for a legal case management system. You have access to case data and insights.
            You can help users understand case trends, analyze performance metrics, and provide recommendations.

            Previous conversation:
            {history}

            Human: {input}
            AI Assistant:"""
        )
        
        # Create the conversation chain
        self.conversation = ConversationChain(
            llm=self.chat,
            memory=self.memory,
            prompt=self.prompt,
            verbose=True
        )
    
    def _initialize_chat_model(self):
        """Initialize the chat model with OpenAI first, then fall back to Gemini (free)."""
        openai_key = os.getenv("OPENAI_API_KEY")
        gemini_key = os.getenv("GEMINI_API_KEY")
        
        if openai_key:
            try:
                return ChatOpenAI(
                    model_name="gpt-3.5-turbo",
                    temperature=0.7,
                )
            except Exception as e:
                print(f"Error initializing OpenAI: {str(e)}")
                print("Falling back to Gemini...")
        
        if gemini_key:
            try:
                return ChatGoogleGenerativeAI(
                    model="gemini-2.0-flash",
                    google_api_key=gemini_key,
                    temperature=0.7,
                )
            except Exception as e:
                print(f"Error initializing Gemini: {str(e)}")
                if openai_key:
                    raise Exception("Both OpenAI and Gemini failed to initialize. Please check your API keys.")
                else:
                    raise Exception("Gemini failed to initialize. Please check your API key.")
        
        raise Exception("No API keys found. Please configure either OpenAI (paid) or Gemini (free) API key.")
    
    def _fetch_case_data(self):
        """Fetch case data from the API."""
        try:
            response = requests.get(f"{self.api_url}/cases")
            if response.status_code == 200:
                return pd.DataFrame(response.json())
            return None
        except Exception as e:
            print(f"Error fetching case data: {str(e)}")
            return None
    
    def _fetch_metrics(self):
        """Fetch metrics from the API."""
        try:
            response = requests.get(f"{self.api_url}/metrics")
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Error fetching metrics: {str(e)}")
            return None
    
    def _fetch_insights(self):
        """Fetch insights from the API."""
        try:
            response = requests.get(f"{self.api_url}/insights")
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Error fetching insights: {str(e)}")
            return None
    
    def get_response(self, user_input: str) -> str:
        """Get a response from the chatbot based on user input."""
        # Fetch latest data
        cases_df = self._fetch_case_data()
        metrics = self._fetch_metrics()
        insights = self._fetch_insights()
        
        # Add context to the conversation
        context = "Here's the current system state:\n"
        if metrics:
            context += f"""
            - Total Cases: {metrics['total_cases']}
            - Active Cases: {metrics['active_cases']}
            - Resolved Cases: {metrics['resolved_cases']}
            - Escalation Rate: {metrics['escalation_rate']}
            """
        
        if insights:
            context += "\nKey Insights:\n"
            for insight in insights['insights']:
                context += f"- {insight}\n"
        
        # Combine context with user input
        full_input = f"{context}\n\nUser Question: {user_input}"
        
        # Get response from the conversation chain
        response = self.conversation.predict(input=full_input)
        return response
    
    def reset_conversation(self):
        """Reset the conversation history."""
        self.memory.clear() 