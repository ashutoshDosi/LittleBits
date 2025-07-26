#!/usr/bin/env python3
"""
test_demo_working.py
Quick test to verify the demo endpoints are working.
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_demo_auth():
    """Test the demo authentication endpoint."""
    print("🔐 Testing Demo Authentication...")
    try:
        response = requests.post(f"{BASE_URL}/demo/auth")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Auth successful! Token: {data['access_token']}")
            return data['access_token']
        else:
            print(f"❌ Auth failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Auth error: {e}")
        return None

def test_demo_chat(message):
    """Test the demo chat endpoint."""
    print(f"💬 Testing Chat: '{message}'")
    try:
        response = requests.post(
            f"{BASE_URL}/demo/chat",
            headers={"Content-Type": "application/json"},
            json={"message": message}
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Chat successful!")
            print(f"🤖 Response: {data['response'][:100]}...")
            return True
        else:
            print(f"❌ Chat failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Chat error: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing CycleWise Demo Endpoints\n")
    
    # Test authentication
    token = test_demo_auth()
    if not token:
        print("❌ Cannot proceed without authentication")
        return
    
    print()
    
    # Test chat messages
    test_messages = [
        "I have cramps and feel tired",
        "I feel moody and bloated",
        "What should I eat during my period?",
        "How can I track my cycle better?",
        "I'm feeling stressed about my symptoms"
    ]
    
    for message in test_messages:
        test_demo_chat(message)
        print()
    
    print("🎉 All tests completed!")
    print("\n📋 Next Steps:")
    print("1. Open mock_frontend.html in your browser")
    print("2. Click 'Login with Google'")
    print("3. Try the demo buttons or type your own messages")
    print("4. Your backend is ready for the hackathon! 🚀")

if __name__ == "__main__":
    main() 