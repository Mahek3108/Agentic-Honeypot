#!/usr/bin/env python3
"""
Test script to verify API response format matches GUVI requirements.
Usage: python test_api.py
"""

import json
import requests

# CHANGE THESE TO YOUR ACTUAL VALUES
API_URL = "http://localhost:8000/honeypot" # Your deployed API URL
API_KEY = "changeme"  # Your API key

def test_first_message():
    """Test with first scam message (no conversation history)"""
    
    payload = {
        "sessionId": "test-session-001",
        "message": {
            "sender": "scammer",
            "text": "Your bank account will be blocked today. Verify immediately at http://fake-bank.com",
            "timestamp": 1770005528731
        },
        "conversationHistory": [],
        "metadata": {
            "channel": "SMS",
            "language": "English",
            "locale": "IN"
        }
    }
    
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    
    print("=" * 70)
    print("TEST 1: First Message (Scam Detection)")
    print("=" * 70)
    print(f"\nRequest URL: {API_URL}")
    print(f"Payload:\n{json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(API_URL, json=payload, headers=headers, timeout=15)
        
        print(f"\n✅ Status Code: {response.status_code}")
        print(f"✅ Content-Type: {response.headers.get('Content-Type')}")
        print(f"\n📄 Response Body:")
        print(response.text)
        
        # Parse and validate
        data = response.json()
        print(f"\n📦 Parsed JSON:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        
        # Validate required fields
        print(f"\n🔍 Validation:")
        assert "status" in data, "❌ Missing 'status' field"
        assert "reply" in data, "❌ Missing 'reply' field"
        assert data["status"] == "success", "❌ Status is not 'success'"
        assert isinstance(data["reply"], str), "❌ Reply is not a string"
        assert len(data["reply"]) > 0, "❌ Reply is empty"
        
        # Check for extra fields (should only have status and reply)
        expected_fields = {"status", "reply"}
        actual_fields = set(data.keys())
        extra_fields = actual_fields - expected_fields
        
        if extra_fields:
            print(f"⚠️  Warning: Extra fields found: {extra_fields}")
            print("   GUVI expects ONLY 'status' and 'reply'")
        else:
            print("✅ Response has exactly 2 fields: status and reply")
        
        print("\n✅ TEST 1 PASSED!")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Request failed: {e}")
        return False
    except json.JSONDecodeError as e:
        print(f"\n❌ Invalid JSON response: {e}")
        return False
    except AssertionError as e:
        print(f"\n❌ Validation failed: {e}")
        return False


def test_follow_up_message():
    """Test with follow-up message (with conversation history)"""
    
    payload = {
        "sessionId": "test-session-002",
        "message": {
            "sender": "scammer",
            "text": "Share your UPI ID to avoid account suspension. Use this: scammer@paytm",
            "timestamp": 1770005538731
        },
        "conversationHistory": [
            {
                "sender": "scammer",
                "text": "Your account is blocked",
                "timestamp": 1770005528731
            },
            {
                "sender": "user",
                "text": "Why is it blocked?",
                "timestamp": 1770005533731
            }
        ],
        "metadata": {
            "channel": "WhatsApp",
            "language": "English",
            "locale": "IN"
        }
    }
    
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    
    print("\n\n" + "=" * 70)
    print("TEST 2: Follow-up Message (Intelligence Extraction)")
    print("=" * 70)
    print(f"\nPayload:\n{json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(API_URL, json=payload, headers=headers, timeout=15)
        
        print(f"\n✅ Status Code: {response.status_code}")
        data = response.json()
        print(f"\n📦 Parsed JSON:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        
        assert "status" in data and "reply" in data
        print("\n✅ TEST 2 PASSED!")
        return True
        
    except Exception as e:
        print(f"\n❌ TEST 2 FAILED: {e}")
        return False


def test_casual_message():
    """Test with non-scam message"""
    
    payload = {
        "sessionId": "test-session-003",
        "message": {
            "sender": "user",
            "text": "Hello, how are you?",
            "timestamp": 1770005528731
        },
        "conversationHistory": [],
        "metadata": {
            "channel": "SMS",
            "language": "English",
            "locale": "IN"
        }
    }
    
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
        }
    
    print("\n\n" + "=" * 70)
    print("TEST 3: Casual Message (Non-Scam)")
    print("=" * 70)
    
    try:
        response = requests.post(API_URL, json=payload, headers=headers, timeout=15)
        data = response.json()
        print(f"\n📦 Response:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        
        assert "status" in data and "reply" in data
        print("\n✅ TEST 3 PASSED!")
        return True
        
    except Exception as e:
        print(f"\n❌ TEST 3 FAILED: {e}")
        return False


if __name__ == "__main__":
    print("\n" + "🚀 Starting API Tests" + "\n")
    
    if API_URL == "https://your-api-url.com/honeypot":
        print("❌ ERROR: Please update API_URL in the script with your actual API URL")
        exit(1)
    
    if API_KEY == "your-api-key-here":
        print("❌ ERROR: Please update API_KEY in the script with your actual API key")
        exit(1)
    
    results = []
    results.append(("First Message Test", test_first_message()))
    results.append(("Follow-up Message Test", test_follow_up_message()))
    results.append(("Casual Message Test", test_casual_message()))
    
    print("\n\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    all_passed = all(result[1] for result in results)
    
    if all_passed:
        print("\n🎉 All tests passed! Your API is ready for GUVI evaluation.")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")