"""
Test script for the Case AI Analytics API

This script tests all endpoints of the Case AI Analytics API to ensure that they
are working correctly. It provides a comprehensive verification that the server
is running properly and all functionality is available.

Usage:
    python -m tests.test_api

The script will test:
1. Root endpoint (/) - Basic connectivity and welcome message
2. Prediction endpoint (/predict) - Case resolution prediction
3. Insights endpoint (/insights) - Data insights extraction
"""
import requests
import json
import sys
import time

# Wait a moment for the server to start
print("Waiting for server to start...")
time.sleep(3)

# Set the API base URL
BASE_URL = "http://localhost:5000"
# Alternative URL for remote access
# BASE_URL = "http://154.0.164.254:5000"

def test_root_endpoint():
    """
    Test the root endpoint
    
    Verifies that the server is running and responds to basic requests.
    This is a simple connectivity test that should always pass if the
    server is running correctly.
    """
    print("\n===== Testing Root Endpoint =====")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=10)
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("✅ Test passed")
            return True
        else:
            print("❌ Test failed")
            return False
    except Exception as e:
        print(f"Error: {e}")
        print("❌ Test failed - Is the server running?")
        return False

def test_predict_endpoint():
    """
    Test the prediction endpoint
    
    Verifies that the prediction endpoint can process a case prediction request
    and return a valid response with prediction results.
    """
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
            json=case_data,
            timeout=10
        )
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Response: {json.dumps(result, indent=2)}")
            
            # Verify that the response contains expected fields
            if "prediction" in result and "probability" in result:
                print(f"Prediction: {result['prediction']}")
                print(f"Probability: {result['probability']:.4f}")
                print("✅ Test passed")
                return True
            else:
                print("❌ Test failed: Response missing expected fields")
                return False
        else:
            print(f"Error response: {response.text}")
            print("❌ Test failed")
            return False
    except Exception as e:
        print(f"Error: {e}")
        print("❌ Test failed")
        return False

def test_insights_endpoint():
    """
    Test the insights endpoint
    
    Verifies that the insights endpoint can process a request for case insights
    and return valid analytical data about case types.
    """
    print("\n===== Testing Insights Endpoint =====")
    
    insights_data = {
        "insight_type": "common_case_types"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/insights",
            headers={"Content-Type": "application/json"},
            json=insights_data,
            timeout=10
        )
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Response: {json.dumps(result, indent=2)}")
            print("✅ Test passed")
            return True
        else:
            print(f"Error response: {response.text}")
            print("❌ Test failed")
            return False
    except Exception as e:
        print(f"Error: {e}")
        print("❌ Test failed")
        return False

def main():
    """
    Run all tests and provide a summary of results
    
    Executes all test functions and reports on their success or failure.
    Returns an exit code that can be used by CI/CD systems to determine
    if the tests passed or failed.
    """
    print("Starting API tests...")
    
    all_tests_pass = True
    
    # Run each test and track results
    root_test_passed = test_root_endpoint()
    if not root_test_passed:
        all_tests_pass = False
    
    predict_test_passed = test_predict_endpoint()
    if not predict_test_passed:
        all_tests_pass = False
    
    insights_test_passed = test_insights_endpoint()
    if not insights_test_passed:
        all_tests_pass = False
    
    # Print summary
    print("\n===== Test Summary =====")
    print(f"Root Endpoint:     {'✅ Passed' if root_test_passed else '❌ Failed'}")
    print(f"Predict Endpoint:  {'✅ Passed' if predict_test_passed else '❌ Failed'}")
    print(f"Insights Endpoint: {'✅ Passed' if insights_test_passed else '❌ Failed'}")
    
    if all_tests_pass:
        print("\nAll tests passed! ✅")
        return 0
    else:
        print("\nSome tests failed. ❌ Check the output above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
