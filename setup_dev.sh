#!/bin/bash

echo "🔧 Setting up Development Environment"
echo "====================================="

# Create .env file for backend
echo "📝 Creating backend .env file..."
cat > backend/.env << EOF
# Development Mode (set to True to disable rate limiting for testing)
DEV_MODE=True

# OpenAI API Configuration (optional - will use simulation mode if not set)
# OPENAI_API_KEY=your_openai_api_key_here

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True

# Rate Limiting
RATE_LIMIT_PER_MINUTE=30
RATE_LIMIT_PER_HOUR=100
EOF

echo "✅ Development environment configured!"
echo ""
echo "🚀 To start the application:"
echo "   ./start.sh"
echo ""
echo "🧪 To test the backend:"
echo "   python test_backend.py"
echo ""
echo "📱 Frontend will be available at: http://localhost:3000"
echo "🔧 Backend will be available at: http://localhost:5000"
