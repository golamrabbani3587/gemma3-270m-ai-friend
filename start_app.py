#!/usr/bin/env python3
"""
Startup script for AI Chat Companion
Runs both the API server and web server
"""

import subprocess
import time
import sys
import os
from threading import Thread

def run_api_server():
    """Run the FastAPI server"""
    print("🚀 Starting API server on port 8001...")
    subprocess.run([sys.executable, "api_server.py"])

def run_web_server():
    """Run the web server"""
    print("🌐 Starting web server on port 3000...")
    subprocess.run([sys.executable, "web_server.py"])

def main():
    print("💖 Starting AI Chat Companion...")
    print("=" * 50)
    
    # Check if static directory exists
    if not os.path.exists("static"):
        print("❌ Error: static directory not found!")
        print("Please make sure the static/index.html file exists.")
        return
    
    # Start API server in a separate thread
    api_thread = Thread(target=run_api_server, daemon=True)
    api_thread.start()
    
    # Wait a moment for API server to start
    time.sleep(3)
    
    # Start web server in main thread
    run_web_server()

if __name__ == "__main__":
    main()
