#!/usr/bin/env python3
"""
test_backend.py
Simple script to test your backend endpoints.
"""

import requests
import json
import time

# Configuration
BACKEND_URL = "http://localhost:8000"

def test_backend_health():
    """Test if the backend is running."""
    try:
        response = requests.get(f"{BACKEND_URL}/docs")
        if response.status_code == 200:
            print("✅ Backend is running!")
            return True
        else:
            print(f"❌ Backend returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend is not running. Start it with: uvicorn src.main:app --reload")
        return False

def test_google_auth():
    """Test Google OAuth endpoint."""
    try:
        # Mock Google token
        mock_token = f"mock-google-token-{int(time.time())}"
        
        response = requests.post(
            f"{BACKEND_URL}/api/auth/google",
            json={"token": mock_token},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Google auth endpoint working!")
            print(f"   Received token: {data['access_token'][:20]}...")
            return data['access_token']
        else:
            print(f"❌ Google auth failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Google auth error: {e}")
        return None

def test_chat_endpoint(access_token):
    """Test the chat endpoint."""
    try:
        response = requests.post(
            f"{BACKEND_URL}/chat",
            json={"message": "I have cramps and feel tired"},
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}"
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Chat endpoint working!")
            print(f"   Response: {data['response'][:100]}...")
            return True
        else:
            print(f"❌ Chat endpoint failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Chat endpoint error: {e}")
        return False

def test_api_endpoints(access_token):
    """Test other API endpoints."""
    endpoints = [
        ("/api/me", "GET"),
        ("/api/interactions", "GET"),
        ("/api/cycles", "GET"),
        ("/api/reminders", "GET"),
    ]
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    for endpoint, method in endpoints:
        try:
            if method == "GET":
                response = requests.get(f"{BACKEND_URL}{endpoint}", headers=headers)
            else:
                response = requests.post(f"{BACKEND_URL}{endpoint}", headers=headers)
            
            if response.status_code in [200, 201]:
                print(f"✅ {endpoint} working!")
            else:
                print(f"⚠️  {endpoint} returned {response.status_code}")
        except Exception as e:
            print(f"❌ {endpoint} error: {e}")

def main():
    """Run all backend tests."""
    print("🧪 Testing CycleWise Backend...\n")
    
    # Test 1: Backend health
    if not test_backend_health():
        return
    
    print("\n" + "="*50)
    
    # Test 2: Google OAuth
    access_token = test_google_auth()
    if not access_token:
        print("❌ Cannot proceed without authentication")
        return
    
    print("\n" + "="*50)
    
    # Test 3: Chat endpoint
    test_chat_endpoint(access_token)
    
    print("\n" + "="*50)
    
    # Test 4: Other API endpoints
    print("Testing other API endpoints...")
    test_api_endpoints(access_token)
    
    print("\n" + "="*50)
    print("🎉 Backend testing complete!")
    print("\n📋 Next steps:")
    print("1. Open mock_frontend.html in your browser")
    print("2. Click 'Login with Google'")
    print("3. Try the demo buttons or type your own messages")
    print("4. Check the backend logs to see the ReAct reasoning process")

if __name__ == "__main__":
    main() 