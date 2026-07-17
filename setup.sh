#!/bin/bash

# Dil Se Quick Start Script
# Run this script to set up the app

echo "🌟 Dil Se - Mental Wellness Companion Setup 🌟"
echo ""
echo "This script will set up your development environment"
echo ""

# Step 1: Check Python
echo "1️⃣  Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python 3.8+"
    exit 1
fi
python_version=$(python3 --version)
echo "✅ Found: $python_version"
echo ""

# Step 2: Create virtual environment
echo "2️⃣  Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi
echo ""

# Step 3: Activate virtual environment
echo "3️⃣  Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Step 4: Install dependencies
echo "4️⃣  Installing dependencies..."
pip install -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Step 5: Create .env file
echo "5️⃣  Setting up environment variables..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✅ Created .env file"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env and add your Anthropic API key:"
    echo "   ANTHROPIC_API_KEY=sk-ant-..."
    echo ""
else
    echo "✅ .env file already exists"
    echo ""
fi

# Step 6: Initialize database
echo "6️⃣  Initializing database..."
python3 -c "
from app import app, db
with app.app_context():
    db.create_all()
    print('✅ Database initialized')
"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 Setup complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your Anthropic API key"
echo "2. Run: python app.py"
echo "3. Open: http://localhost:5000"
echo ""
echo "For more info, see README.md or PROJECT_DOCUMENTATION.md"
echo ""
