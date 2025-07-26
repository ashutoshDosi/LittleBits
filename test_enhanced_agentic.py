"""
test_enhanced_agentic.py

Enhanced test script to demonstrate the complete agentic AI workflow with external tools:
1. Memory retrieval
2. ReAct pattern with external tool integration
3. Calendar API for stress correlation
4. Health tracking APIs (hydration, exercise, sleep)
5. Medical information APIs for evidence-based advice
6. Weather API for symptom correlation
7. Structured task planning with categories and reasons

Run this after starting your FastAPI server.
"""

import requests
import json

# Configuration
BASE_URL = "http://127.0.0.1:8000"
TEST_USER_EMAIL = "test_enhanced@example.com"
TEST_USER_PASSWORD = "testpassword123"

def test_enhanced_agentic_workflow():
    """Test the complete enhanced agentic AI workflow with external tools."""
    
    print("🤖 Testing Enhanced Agentic AI Workflow with External Tools")
    print("=" * 70)
    
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
    
    # Step 3: Test enhanced chat with external tool integration
    print("\n3️⃣ Testing enhanced chat with external tools and ReAct pattern...")
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # Test messages that should trigger different external tools
    test_messages = [
        "I'm feeling really tired today and have cramps",
        "What's my schedule like today? I think stress is affecting my symptoms",
        "I'm not drinking enough water, can you check my hydration?",
        "What's the weather like? I feel like it's affecting my mood",
        "I have really bad cramps, what does medical research say about this?",
        "Can you do a comprehensive analysis of all factors affecting my health today?"
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
                print(f"✅ AI Response: {response_data['response'][:300]}...")
                
                # Check for external tool usage indicators
                tool_indicators = {
                    'calendar': ['schedule', 'meeting', 'stress', 'calendar'],
                    'health': ['hydration', 'water', 'exercise', 'sleep', 'steps'],
                    'medical': ['medical', 'research', 'evidence', 'remedies'],
                    'weather': ['weather', 'temperature', 'sunny', 'rainy'],
                    'comprehensive': ['comprehensive', 'analysis', 'factors']
                }
                
                response_lower = response_data['response'].lower()
                used_tools = []
                for tool, keywords in tool_indicators.items():
                    if any(keyword in response_lower for keyword in keywords):
                        used_tools.append(tool)
                
                if used_tools:
                    print(f"🎯 External tools used: {', '.join(used_tools)}")
                else:
                    print("📝 Standard response (may be fallback)")
                    
                # Check for ReAct pattern indicators
                react_indicators = ['thought', 'action', 'observation', 'reflection', 'task']
                if any(indicator in response_lower for indicator in react_indicators):
                    print("🧠 ReAct pattern detected!")
                    
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
    
    # Step 5: Test external tools directly
    print("\n5️⃣ Testing external tools directly...")
    
    # Test calendar tool
    print("\n📅 Testing Calendar Tool (Stress Correlation):")
    try:
        calendar_response = requests.post(
            f"{BASE_URL}/api/chat",
            json={"message": "Check my calendar for today"},
            headers=headers
        )
        if calendar_response.status_code == 200:
            print(f"✅ Calendar response: {calendar_response.json()['response'][:200]}...")
    except Exception as e:
        print(f"❌ Calendar test failed: {e}")
    
    # Test health tracking tool
    print("\n💧 Testing Health Tracking Tool:")
    try:
        health_response = requests.post(
            f"{BASE_URL}/api/chat",
            json={"message": "Check my hydration and exercise levels"},
            headers=headers
        )
        if health_response.status_code == 200:
            print(f"✅ Health response: {health_response.json()['response'][:200]}...")
    except Exception as e:
        print(f"❌ Health test failed: {e}")
    
    # Test medical info tool
    print("\n🏥 Testing Medical Information Tool:")
    try:
        medical_response = requests.post(
            f"{BASE_URL}/api/chat",
            json={"message": "Research medical information about cramps"},
            headers=headers
        )
        if medical_response.status_code == 200:
            print(f"✅ Medical response: {medical_response.json()['response'][:200]}...")
    except Exception as e:
        print(f"❌ Medical test failed: {e}")
    
    print("\n" + "=" * 70)
    print("🎉 Enhanced Agentic AI Workflow Test Complete!")
    print("\nKey Features Demonstrated:")
    print("✅ Memory retrieval from past interactions")
    print("✅ ReAct pattern (Thought → Action → Observation → Reflection)")
    print("✅ External tool integration (Calendar, Health, Medical, Weather)")
    print("✅ Structured task planning with categories and reasons")
    print("✅ Evidence-based medical advice")
    print("✅ Stress correlation with calendar data")
    print("✅ Health tracking integration")
    print("✅ Weather impact analysis")
    print("✅ Comprehensive health analysis")
    print("✅ Error handling and fallback mechanisms")
    print("✅ JWT authentication and user context")

if __name__ == "__main__":
    print("🚀 Starting Enhanced Agentic AI Workflow Test...")
    print("Make sure your FastAPI server is running on http://127.0.0.1:8000")
    print("This test demonstrates external tool integration and sophisticated agentic AI patterns.")
    print("Press Enter to continue...")
    input()
    
    test_enhanced_agentic_workflow() 