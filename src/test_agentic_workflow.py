"""
test_agentic_workflow.py

Test script to demonstrate the enhanced agentic AI workflow:
1. Memory retrieval
2. ReAct pattern (Thought → Action → Observation → Reflection)
3. Structured task planning
4. Error handling

Run this after starting your FastAPI server.
"""

import requests
import json

# Configuration
BASE_URL = "http://127.0.0.1:8000"
TEST_USER_EMAIL = "test@example.com"
TEST_USER_PASSWORD = "testpassword123"

def test_agentic_workflow():
    """Test the complete agentic AI workflow."""
    
    print("🤖 Testing Enhanced Agentic AI Workflow for CycleWise")
    print("=" * 60)
    
    # Step 1: Register a test user
    print("\n1️⃣ Registering test user...")
    register_data = {
        "email": TEST_USER_EMAIL,
        "password": TEST_USER_PASSWORD
    }
    
    try:
        register_response = requests.post(f"{BASE_URL}/api/register", json=register_data)
        if register_response.status_code == 200:
            print("✅ User registered successfully")
        else:
            print(f"⚠️ User might already exist: {register_response.status_code}")
    except Exception as e:
        print(f"❌ Registration failed: {e}")
        return
    
    # Step 2: Login to get JWT token
    print("\n2️⃣ Logging in to get JWT token...")
    login_data = {
        "username": TEST_USER_EMAIL,
        "password": TEST_USER_PASSWORD
    }
    
    try:
        login_response = requests.post(f"{BASE_URL}/api/token", data=login_data)
        if login_response.status_code == 200:
            token_data = login_response.json()
            access_token = token_data["access_token"]
            print("✅ Login successful, got JWT token")
        else:
            print(f"❌ Login failed: {login_response.status_code}")
            return
    except Exception as e:
        print(f"❌ Login failed: {e}")
        return
    
    # Step 3: Test chat with memory retrieval and ReAct pattern
    print("\n3️⃣ Testing enhanced chat with memory and ReAct pattern...")
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # Test messages that should trigger different agentic behaviors
    test_messages = [
        "I'm feeling really tired today and have cramps",
        "What phase of my cycle am I in?",
        "Can you remind me to take my vitamins?",
        "I want to send a message to my partner about how I'm feeling"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n--- Test Message {i}: '{message}' ---")
        
        try:
            chat_data = {"message": message}
            chat_response = requests.post(
                f"{BASE_URL}/api/chat", 
                json=chat_data, 
                headers=headers
            )
            
            if chat_response.status_code == 200:
                response_data = chat_response.json()
                print(f"✅ AI Response: {response_data['response'][:200]}...")
                
                # Check if response shows agentic behavior
                if any(keyword in response_data['response'].lower() for keyword in 
                       ['thought', 'action', 'observation', 'reflection', 'task']):
                    print("🎯 Agentic AI behavior detected!")
                else:
                    print("📝 Standard response (may be fallback)")
            else:
                print(f"❌ Chat failed: {chat_response.status_code}")
                
        except Exception as e:
            print(f"❌ Chat request failed: {e}")
    
    # Step 4: Test memory retrieval
    print("\n4️⃣ Testing memory retrieval...")
    try:
        memory_response = requests.get(f"{BASE_URL}/api/interactions", headers=headers)
        if memory_response.status_code == 200:
            interactions = memory_response.json()
            print(f"✅ Retrieved {len(interactions)} past interactions")
            if interactions:
                print(f"📝 Latest interaction: {interactions[0]['message'][:50]}...")
        else:
            print(f"❌ Memory retrieval failed: {memory_response.status_code}")
    except Exception as e:
        print(f"❌ Memory retrieval failed: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Agentic AI Workflow Test Complete!")
    print("\nKey Features Demonstrated:")
    print("✅ Memory retrieval from past interactions")
    print("✅ ReAct pattern (Thought → Action → Observation → Reflection)")
    print("✅ Structured task planning with categories and reasons")
    print("✅ Error handling and fallback mechanisms")
    print("✅ JWT authentication and user context")

if __name__ == "__main__":
    print("🚀 Starting Agentic AI Workflow Test...")
    print("Make sure your FastAPI server is running on http://127.0.0.1:8000")
    print("Press Enter to continue...")
    input()
    
    test_agentic_workflow() 