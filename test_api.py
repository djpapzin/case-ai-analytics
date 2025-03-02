"""
Test script for the Case AI Analytics API
"""
import requests
import json
import sys

# Set the API base URL
BASE_URL = "http://localhost:5000"
# Alternative URL for remote access
# BASE_URL = "http://154.0.164.254:5000"

def test_root_endpoint():
    """Test the root endpoint"""
    print("\n===== Testing Root Endpoint =====")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_predict_endpoint():
    """Test the prediction endpoint"""
    print("\n===== Testing Predict Endpoint =====")
    
    case_data = {
        "case_type": "Family Law",
        "complexity": "Medium",
        "client_age": 35,
        "client_income_level": "Medium",
        "days_open": 30,
        "escalated": False
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/predict",
            headers={"Content-Type": "application/json"},
            json=case_data
        )
        print(f"Status code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_insights_endpoint():
    """Test the insights endpoint"""
    print("\n===== Testing Insights Endpoint =====")
    
    insights_data = {
        "insight_type": "common_case_types"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/insights",
            headers={"Content-Type": "application/json"},
            json=insights_data
        )
        print(f"Status code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    """Run all tests"""
    print("Starting API tests...")
    
    all_tests_pass = True
    
    if not test_root_endpoint():
        all_tests_pass = False
    
    if not test_predict_endpoint():
        all_tests_pass = False
    
    if not test_insights_endpoint():
        all_tests_pass = False
    
    print("\n===== Test Summary =====")
    if all_tests_pass:
        print("All tests passed!")
        return 0
    else:
        print("Some tests failed. Check the output above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
