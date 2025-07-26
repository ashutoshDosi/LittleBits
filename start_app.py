#!/usr/bin/env python3
"""
start_app.py
Startup script for CycleWise application.
Starts both backend and frontend servers.
"""

import subprocess
import sys
import os
import time
import signal
import threading
from pathlib import Path

def start_backend():
    """Start the FastAPI backend server."""
    print("🚀 Starting CycleWise Backend...")
    try:
        # Change to src directory and start uvicorn
        os.chdir("src")
        process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", "main:app", 
            "--host", "0.0.0.0", "--port", "8000", "--reload"
        ])
        return process
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        return None

def start_frontend():
    """Start the Next.js frontend server."""
    print("🎨 Starting CycleWise Frontend...")
    try:
        # Change to frontend directory and start Next.js
        os.chdir("src/frontend")
        process = subprocess.Popen([
            "npm", "run", "dev"
        ])
        return process
    except Exception as e:
        print(f"❌ Error starting frontend: {e}")
        return None

def main():
    """Main function to start both servers."""
    print("=" * 60)
    print("🌟 CycleWise - Menstrual Health Companion")
    print("=" * 60)
    print()
    
    # Check if .env file exists
    if not os.path.exists(".env"):
        print("⚠️  Warning: .env file not found!")
        print("   Please create a .env file with your API keys:")
        print("   - GEMINI_API_KEY")
        print("   - SECRET_KEY")
        print("   - GOOGLE_CLIENT_ID")
        print("   - GOOGLE_CLIENT_SECRET")
        print()
    
    # Store original directory
    original_dir = os.getcwd()
    
    # Start backend
    backend_process = start_backend()
    if not backend_process:
        print("❌ Failed to start backend. Exiting.")
        return
    
    # Wait a moment for backend to start
    time.sleep(3)
    
    # Start frontend
    os.chdir(original_dir)  # Go back to root
    frontend_process = start_frontend()
    if not frontend_process:
        print("❌ Failed to start frontend. Stopping backend.")
        backend_process.terminate()
        return
    
    print()
    print("✅ Both servers started successfully!")
    print()
    print("🌐 Frontend: http://localhost:3000")
    print("🔧 Backend API: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print()
    print("Press Ctrl+C to stop both servers")
    print()
    
    try:
        # Wait for both processes
        while True:
            time.sleep(1)
            # Check if processes are still running
            if backend_process.poll() is not None:
                print("❌ Backend server stopped unexpectedly")
                break
            if frontend_process.poll() is not None:
                print("❌ Frontend server stopped unexpectedly")
                break
    except KeyboardInterrupt:
        print("\n🛑 Stopping servers...")
        
        # Terminate processes
        if backend_process:
            backend_process.terminate()
        if frontend_process:
            frontend_process.terminate()
        
        # Wait for processes to terminate
        if backend_process:
            backend_process.wait()
        if frontend_process:
            frontend_process.wait()
        
        print("✅ Servers stopped successfully!")

if __name__ == "__main__":
    main() 