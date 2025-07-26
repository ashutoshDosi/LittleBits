#!/usr/bin/env python3
"""
test_demo.py
Quick test script to verify core functionality for hackathon demo.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_gemini_integration():
    """Test Gemini API integration."""
    try:
        from src.executor import call_gemini
        response = call_gemini("Hello! Can you help me with menstrual health?")
        print("✅ Gemini API working!")
        print(f"Response: {response[:100]}...")
        return True
    except Exception as e:
        print(f"❌ Gemini API failed: {e}")
        return False

def test_planner():
    """Test the ReAct planner."""
    try:
        from src.planner import plan_tasks
        tasks = plan_tasks("I have cramps and feel tired")
        print("✅ Planner working!")
        print(f"Generated {len(tasks)} tasks")
        for task in tasks:
            print(f"  - {task['task']} ({task['category']})")
        return True
    except Exception as e:
        print(f"❌ Planner failed: {e}")
        return False

def test_external_tools():
    """Test external tools (mock mode)."""
    try:
        from src.external_tools import CalendarTool, HealthTrackingTool, MedicalInfoTool
        
        # Test calendar
        calendar = CalendarTool.get_user_schedule(1)
        print("✅ Calendar tool working!")
        
        # Test health tracking
        health = HealthTrackingTool.get_health_data(1)
        print("✅ Health tracking tool working!")
        
        # Test medical info
        medical = MedicalInfoTool.get_medical_info("cramps", "menstrual")
        print("✅ Medical info tool working!")
        
        return True
    except Exception as e:
        print(f"❌ External tools failed: {e}")
        return False

def test_environment():
    """Test environment variables."""
    required_vars = ['GEMINI_API_KEY', 'SECRET_KEY', 'GOOGLE_CLIENT_ID']
    missing = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)
    
    if missing:
        print(f"❌ Missing environment variables: {missing}")
        return False
    else:
        print("✅ All environment variables set!")
        return True

def main():
    """Run all tests."""
    print("🧪 Testing CycleWise Backend for Hackathon Demo...\n")
    
    tests = [
        ("Environment Variables", test_environment),
        ("Gemini API Integration", test_gemini_integration),
        ("ReAct Planner", test_planner),
        ("External Tools", test_external_tools),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Testing {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"   ⚠️  {test_name} needs attention")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your backend is ready for the hackathon demo!")
        print("\n🚀 Next steps:")
        print("1. Start your server: uvicorn src.main:app --reload")
        print("2. Test the /chat endpoint with a POST request")
        print("3. Record your demo showing the ReAct reasoning process!")
    else:
        print("⚠️  Some tests failed. Please fix the issues before your demo.")
        sys.exit(1)

if __name__ == "__main__":
    main() 