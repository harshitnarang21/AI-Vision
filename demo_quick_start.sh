#!/bin/bash

# Quick demo preparation script

echo "🎬 Preparing for AI Navigation Assistant Demo..."
echo ""

# Check if app is running
if lsof -Pi :5001 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "✓ Application is already running on port 5001"
else
    echo "⚠️  Application is not running"
    echo "   Start it with: ./start.sh"
    echo ""
fi

# Check Azure services
echo "🔍 Checking Azure services..."
source venv/bin/activate 2>/dev/null
python test_connection.py

echo ""
echo "📋 Demo Checklist:"
echo "  [ ] Application running (http://localhost:5001)"
echo "  [ ] Camera access granted"
echo "  [ ] Audio volume up"
echo "  [ ] Sample objects/text ready"
echo "  [ ] Phone ready for mobile demo (optional)"
echo ""
echo "📖 Full demo guide: See DEMO_GUIDE.md"
echo ""
echo "🚀 Ready to demo! Open http://localhost:5001 in your browser"


