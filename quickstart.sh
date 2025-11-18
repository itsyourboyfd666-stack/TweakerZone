#!/bin/bash

echo "==================================="
echo "  Grok-Blackbox Quick Start"
echo "==================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
python3 -m pip install -q requests python-dotenv

# Check if .env exists
if [ ! -f .env ]; then
    echo ""
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ Created .env file. Please edit it with your API keys."
fi

# Run the CLI
echo ""
echo "🚀 Launching Grok-Blackbox CLI..."
echo ""
python3 grok_cli.py

echo ""
echo "✅ Done!"
