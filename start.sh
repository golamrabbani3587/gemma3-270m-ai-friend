#!/bin/bash
echo "Starting AI Chat Companion..."
echo "Current directory: $(pwd)"
echo "Python version: $(python --version)"
echo "Python path: $(which python)"
echo "Files in current directory:"
ls -la

# Try multiple Python commands
if command -v python3 &> /dev/null; then
    echo "Using python3..."
    python3 render_app.py
elif command -v python &> /dev/null; then
    echo "Using python..."
    python render_app.py
else
    echo "Python not found in PATH"
    exit 1
fi
