"""
Test script for the Case AI Analytics prediction endpoint

This script tests the prediction endpoint of the Case AI Analytics API by sending 
various test cases and verifying responses. It helps ensure that the prediction
functionality is working correctly after deployment or code changes.

Usage:
    python -m tests.test_prediction

The script will:
1. Wait for the server to start (3 seconds)
2. Send test cases to the prediction endpoint
3. Display the results for each test case
4. Indicate whether each test passed or failed
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
    """
    Test the prediction endpoint with different cases
    
    This function defines several test cases with different attributes and sends
    them to the prediction endpoint. It then displays the response for each case
    and indicates whether the test passed or failed.
    
    Test cases cover various combinations of:
    - Case types (Family Law, Corporate, Estate Planning)
    - Complexity levels
    - Client demographics
    - Case status (days open, escalation)
    """
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
    
    # Track overall test success
    all_tests_passed = True
    
    # Test each case
    for case in test_cases:
        print(f"\nTesting {case['name']}:")
        try:
            # Send POST request to prediction endpoint
            response = requests.post(
                f"{BASE_URL}/predict",
                headers={"Content-Type": "application/json"},
                json=case['data'],
                timeout=10
            )
            
            # Display response status and details
            print(f"Status code: {response.status_code}")
            
            # Check if request was successful (status code 200)
            if response.status_code == 200:
                result = response.json()
                print(f"Response: {json.dumps(result, indent=2)}")
                
                # Verify that the response contains expected fields
                if "prediction" in result and "probability" in result:
                    print(f"Prediction: {result['prediction']}")
                    print(f"Probability: {result['probability']:.4f}")
                    print("✅ Test passed")
                else:
                    print("❌ Test failed: Response missing expected fields")
                    all_tests_passed = False
            else:
                print(f"Error response: {response.text}")
                print("❌ Test failed")
                all_tests_passed = False
        except Exception as e:
            print(f"Error: {e}")
            print("❌ Test failed")
            all_tests_passed = False
    
    # Print overall test summary
    print("\n===== Test Summary =====")
    if all_tests_passed:
        print("All tests passed! ✅")
    else:
        print("Some tests failed. ❌ Check the output above for details.")
    
    return all_tests_passed

if __name__ == "__main__":
    test_predict() 