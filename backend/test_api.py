#!/usr/bin/env python3
"""
Simple test script for the AI Excel Mock Interviewer API
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_api():
    print("Testing AI Excel Mock Interviewer API...")
    
    # Test 1: Health check
    print("\n1. Testing health check endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
        return False
    
    # Test 2: Start interview
    print("\n2. Testing start interview endpoint...")
    try:
        response = requests.post(f"{BASE_URL}/interview/start")
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Response: {data}")
        interview_id = data.get("interview_id")
        if not interview_id:
            print("Error: No interview_id returned")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False
    
    # Test 3: Submit answers
    print("\n3. Testing submit answer endpoint...")
    test_answers = [
        "VLOOKUP searches vertically in the first column, HLOOKUP searches horizontally in the first row.",
        "I would create a pivot table by selecting the data, going to Insert > PivotTable, then dragging Region to Rows, Product Category to Columns, and Sales to Values.",
        "INDEX returns a value from a specific position, MATCH finds the position of a value. Together they create a flexible lookup that can search in any direction.",
        "I would select the range, go to Home > Conditional Formatting, choose a rule type like 'Highlight Cells Rules' or 'Data Bars' and set the criteria.",
        "I would create a dynamic chart by using a Table (Ctrl+T) for the data source, then creating a chart from that table. As new data is added to the table, the chart updates automatically."
    ]
    
    for i, answer in enumerate(test_answers, 1):
        try:
            response = requests.post(
                f"{BASE_URL}/interview/{interview_id}/answer",
                json={"answer": answer}
            )
            print(f"Answer {i} - Status: {response.status_code}")
            data = response.json()
            print(f"Feedback: {data.get('feedback', 'No feedback')}")
            print(f"Interview completed: {data.get('interview_completed', False)}")
            
            if data.get('interview_completed'):
                break
                
            time.sleep(1)  # Brief pause between questions
            
        except Exception as e:
            print(f"Error submitting answer {i}: {e}")
            return False
    
    # Test 4: Get report
    print("\n4. Testing get report endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/interview/{interview_id}/report")
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Report preview: {data.get('report', 'No report')[:200]}...")
    except Exception as e:
        print(f"Error: {e}")
        return False
    
    print("\n✅ All API tests completed successfully!")
    return True

if __name__ == "__main__":
    test_api()

