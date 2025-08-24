#!/bin/bash

echo "🚀 Deploying AI Friend to Free Hosting"
echo "=================================================="

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Git repository not found. Please initialize git first:"
    echo "   git init"
    echo "   git add ."
    echo "   git commit -m 'Initial commit'"
    exit 1
fi

# Check if remote is set
if ! git remote get-url origin > /dev/null 2>&1; then
    echo "❌ No remote repository found. Please add your GitHub repository:"
    echo "   git remote add origin https://github.com/yourusername/your-repo.git"
    exit 1
fi

echo "✅ Git repository found"
echo "📤 Pushing to GitHub..."

# Push to GitHub
git add .
git commit -m "Deploy AI Friend chat application"
git push origin main

echo "✅ Code pushed to GitHub!"
echo ""
echo "🎯 Next Steps:"
echo "1. Go to https://render.com"
echo "2. Sign up and connect your GitHub repository"
echo "3. Create a new Web Service:"
echo "   - Name: hothasha-api"
echo "   - Environment: Python 3"
echo "   - Build Command: pip install -r requirements.txt"
echo "   - Start Command: python api_server.py"
echo "4. Create a Static Site:"
echo "   - Name: hothasha-web"
echo "   - Build Command: echo 'No build needed'"
echo "   - Publish Directory: static"
echo ""
echo "📖 For detailed instructions, see DEPLOYMENT.md"
echo "🌐 Your app will be live in a few minutes!"
