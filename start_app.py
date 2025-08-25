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
    port = os.environ.get('API_PORT', '8001')
    print(f"🚀 Starting API server on port {port}...")
    env = os.environ.copy()
    env['PORT'] = port
    subprocess.run([sys.executable, "api_server.py"], env=env)

def run_web_server():
    """Run the web server"""
    port = os.environ.get('PORT', '3000')
    print(f"🌐 Starting web server on port {port}...")
    env = os.environ.copy()
    env['PORT'] = port
    env['API_URL'] = f"http://localhost:{os.environ.get('API_PORT', '8001')}"
    subprocess.run([sys.executable, "web_server.py"], env=env)

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
