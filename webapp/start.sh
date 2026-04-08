#!/bin/bash
# Start the Vector-Flow Insight Layer Portal

set -e

echo "🚀 Starting Vector-Flow Insight Layer Portal..."
echo ""

# Check if requirements are installed
python -c "import fastapi" 2>/dev/null || {
    echo "📦 Installing dependencies..."
    pip install -r ../requirements.txt -q
}

echo "✅ Dependencies ready"
echo ""
echo "🌐 Portal will start at: http://localhost:8000"
echo "Press Ctrl+C to stop"
echo ""

# Start the server
cd "$(dirname "$0")"
python app.py
