"""
Test script for the Case AI Analytics prediction endpoint
"""
import requests
import json
import time

# Wait a moment for the server to start
print("Waiting for server to start...")
time.sleep(3)

# Set the API base URL
BASE_URL = "http://localhost:5000"
# Alternative URL for remote access
# BASE_URL = "http://154.0.164.254:5000"

def test_predict():
    """Test the prediction endpoint with different cases"""
    print("\n===== Testing Predict Endpoint =====")
    
    # Define test cases
    test_cases = [
        {
            "name": "Standard Case 1",
            "data": {
                "case_type": "Family Law",
                "complexity": "Medium",
                "client_age": 35,
                "client_income_level": "Medium",
                "days_open": 30,
                "escalated": False
            }
        },
        {
            "name": "Standard Case 2",
            "data": {
                "case_type": "Corporate",
                "complexity": "Medium",
                "client_age": 45,
                "client_income_level": "Medium",
                "days_open": 60,
                "escalated": True
            }
        },
        {
            "name": "Standard Case 3",
            "data": {
                "case_type": "Estate Planning",
                "complexity": "Low",
                "client_age": 25,
                "client_income_level": "Low",
                "days_open": 15,
                "escalated": False
            }
        }
    ]
    
    # Test each case
    for case in test_cases:
        print(f"\nTesting {case['name']}:")
        try:
            response = requests.post(
                f"{BASE_URL}/predict",
                headers={"Content-Type": "application/json"},
                json=case['data'],
                timeout=10
            )
            print(f"Status code: {response.status_code}")
            if response.status_code == 200:
                print(f"Response: {json.dumps(response.json(), indent=2)}")
                print("✅ Test passed")
            else:
                print(f"Error response: {response.text}")
                print("❌ Test failed")
        except Exception as e:
            print(f"Error: {e}")
            print("❌ Test failed")

if __name__ == "__main__":
    test_predict() 