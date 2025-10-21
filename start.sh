#!/bin/bash

# Agentic AI Slack Bot - Start Script

echo "========================================"
echo "Agentic AI Slack Bot"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16 or higher."
    exit 1
fi

echo "✅ Prerequisites check passed"
echo ""

# Install backend dependencies
echo "📦 Installing backend dependencies..."
pip install -r requirements.txt > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Backend dependencies installed"
else
    echo "⚠️  Backend dependencies installation had warnings"
fi
echo ""

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd frontend
npm install > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Frontend dependencies installed"
else
    echo "⚠️  Frontend dependencies installation had warnings"
fi
cd ..
echo ""

# Create .env file if it doesn't exist
if [ ! -f "backend/.env" ]; then
    echo "📝 Creating backend .env file..."
    cp backend/.env.example backend/.env
    echo "✅ .env file created. Please update with your credentials."
    echo ""
fi

# Start backend server
echo "🚀 Starting backend server..."
cd backend
python main.py &
BACKEND_PID=$!
echo "✅ Backend server started on http://localhost:8000 (PID: $BACKEND_PID)"
cd ..
echo ""

# Wait a moment for backend to start
sleep 3

# Start frontend server
echo "🚀 Starting frontend server..."
cd frontend
npm run dev &
FRONTEND_PID=$!
echo "✅ Frontend server started on http://localhost:3000 (PID: $FRONTEND_PID)"
cd ..
echo ""

echo "========================================"
echo "✨ Application is running!"
echo "========================================"
echo ""
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all servers"
echo ""

# Wait for user interrupt
trap "echo ''; echo '🛑 Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo '✅ Servers stopped'; exit 0" INT

# Keep script running
wait
