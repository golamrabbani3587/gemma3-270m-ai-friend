#!/bin/bash

echo "🚀 Starting build process..."

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Set up Hugging Face authentication
echo "🔐 Setting up Hugging Face authentication..."
TOKEN=$HUGGING_FACE_HUB_TOKEN

if [ -z "$TOKEN" ]; then
    echo "❌ Error: HUGGING_FACE_HUB_TOKEN environment variable not set"
    exit 1
fi

# Create .huggingface directory
mkdir -p .huggingface

# Write token to file (this is how huggingface-cli login works)
echo "$TOKEN" > .huggingface/token

echo "✅ Hugging Face authentication configured successfully!"
echo "✅ Build process completed!"
