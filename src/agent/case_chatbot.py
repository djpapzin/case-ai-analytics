from typing import Optional
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv
import pandas as pd
import requests
import google.generativeai as genai

# Load environment variables
load_dotenv()

class CaseChatbot:
    def __init__(self, api_url=None):
        self.api_url = api_url
        self.conversation_history = []
        
        # Get API key from environment
        gemini_key = os.getenv("GEMINI_API_KEY")
        if not gemini_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
            
        # Configure Gemini
        genai.configure(api_key=gemini_key)
        
        # Initialize the chat model
        try:
            self.model = genai.GenerativeModel('gemini-2.0-flash')
            self.chat = self.model.start_chat(history=[])
        except Exception as e:
            print(f"Error initializing chat model: {str(e)}")
            self.chat = None
        
    def get_response_with_context(self, user_input):
        try:
            if not self.chat:
                return "Chat model not initialized. Please check your API key."
                
            # Add user input to conversation history
            self.conversation_history.append({"role": "user", "content": user_input})
            
            # Get response from chat model
            response = self.chat.send_message(user_input)
            
            # Extract just the content from the response
            if hasattr(response, 'text'):
                response_text = response.text
            else:
                # If response is a string containing content=, extract just the content part
                import re
                match = re.search(r"content='([^']*)'", str(response))
                response_text = match.group(1) if match else str(response)
            
            # Add response to conversation history
            self.conversation_history.append({"role": "assistant", "content": response_text})
            
            return response_text
        except Exception as e:
            print(f"Error getting response: {str(e)}")
            return f"I apologize, but I'm currently unable to process your request. Error: {str(e)}"
    
    def reset_conversation(self):
        self.conversation_history = []

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
        """Get response from the chat model using the new LangChain patterns."""
        if not self.chat:
            return ("I apologize, but I'm currently unable to process your request. "
                   "Please check that your GEMINI_API_KEY is correctly set in the environment variables.")

        try:
            # Add user message to history
            self.conversation_history.append({"role": "user", "content": user_input})
            
            # Create a simple response using the chat model directly
            response = self.chat.send_message(user_input)
            
            # Extract just the content from the response
            if hasattr(response, 'text'):
                response_text = response.text
            else:
                # If response is a string containing content=, extract just the content part
                import re
                match = re.search(r"content='([^']*)'", str(response))
                response_text = match.group(1) if match else str(response)
            
            # Add AI response to history
            self.conversation_history.append({"role": "assistant", "content": response_text})
            
            return response_text

        except Exception as e:
            error_msg = f"Error getting response: {str(e)}"
            print(error_msg)
            return ("I apologize, but I encountered an error. Please verify that your Gemini API key is valid. "
                   "Error details: " + str(e))

    def clear_history(self) -> None:
        """Clear conversation history."""
        self.conversation_history = []

    def get_response_with_context(self, user_input: str) -> str:
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
        response = self.get_response(full_input)
        return response 

    def reset_conversation(self) -> None:
        """Reset the conversation history."""
        self.conversation_history = [] 