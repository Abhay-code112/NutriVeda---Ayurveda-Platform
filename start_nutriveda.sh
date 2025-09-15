#!/bin/bash

# NutriVeda Platform Launcher
# Ayurvedic Nutrition Management System

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Unicode symbols
LOTUS="🕉️"
CHECK="✅"
CROSS="❌"
ROCKET="🚀"
GEAR="🔧"
GLOBE="🌐"
STAR="🌟"

echo -e "${CYAN}"
echo "     $LOTUS ===================================$LOTUS"
echo "         NutriVeda Platform Starting..."
echo "         Ayurvedic Nutrition Management"
echo "     $LOTUS ===================================$LOTUS"
echo -e "${NC}"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo -e "${CROSS}${RED} Virtual environment not found!${NC}"
    echo "Please run: python3 setup.py"
    exit 1
fi

# Activate virtual environment
echo -e "${GEAR}${BLUE} Activating virtual environment...${NC}"
source .venv/bin/activate

if [ $? -ne 0 ]; then
    echo -e "${CROSS}${RED} Failed to activate virtual environment${NC}"
    exit 1
fi

echo -e "${CHECK}${GREEN} Virtual environment activated${NC}"

# Function to check if port is available
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null ; then
        return 1
    else
        return 0
    fi
}

# Check if ports are available
if ! check_port 8000; then
    echo -e "${YELLOW}⚠️  Port 8000 is already in use. Please stop the service or choose a different port.${NC}"
    exit 1
fi

if ! check_port 8080; then
    echo -e "${YELLOW}⚠️  Port 8080 is already in use. Please stop the service or choose a different port.${NC}"
    exit 1
fi

# Start backend server
echo ""
echo -e "${GEAR}${BLUE} Starting NutriVeda Backend Server...${NC}"
python backend/app.py &
BACKEND_PID=$!

# Wait for backend to start
echo -e "${YELLOW}⏳ Waiting for backend to initialize...${NC}"
sleep 5

# Check if backend is running
if ! ps -p $BACKEND_PID > /dev/null; then
    echo -e "${CROSS}${RED} Backend failed to start${NC}"
    exit 1
fi

# Start frontend server
echo ""
echo -e "${GLOBE}${BLUE} Starting NutriVeda Frontend Server...${NC}"
python -m http.server 8080 &
FRONTEND_PID=$!

# Wait for frontend to start
echo -e "${YELLOW}⏳ Waiting for frontend to initialize...${NC}"
sleep 3

# Check if frontend is running
if ! ps -p $FRONTEND_PID > /dev/null; then
    echo -e "${CROSS}${RED} Frontend failed to start${NC}"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

echo ""
echo -e "${CHECK}${GREEN} NutriVeda Platform is now running!${NC}"
echo ""
echo -e "${STAR}${CYAN} Access Points:${NC}"
echo -e "   📊 Main Dashboard: ${BLUE}http://localhost:8080/main_dashboard.html${NC}"
echo -e "   🤖 Dosha Analysis: ${BLUE}http://localhost:8080/dosha_detector.html${NC}"
echo -e "   🔧 Backend API:   ${BLUE}http://localhost:8000/api/${NC}"
echo ""
echo -e "${PURPLE}💡 Features Available:${NC}"
echo -e "   ${CHECK} Patient Management System"
echo -e "   ${CHECK} Comprehensive Food Database"
echo -e "   ${CHECK} AI-Powered Dosha Analysis"
echo -e "   ${CHECK} Automated Diet Chart Generation"
echo -e "   ${CHECK} Ayurvedic Nutrition Recommendations"
echo -e "   ${CHECK} Real-time Dashboard Analytics"
echo -e "   ${CHECK} Integrated Chatbot Support"
echo ""

# Try to open the dashboard in default browser (Linux)
if command -v xdg-open > /dev/null; then
    echo -e "${ROCKET}${GREEN} Opening NutriVeda Dashboard...${NC}"
    sleep 2
    xdg-open "http://localhost:8080/main_dashboard.html" 2>/dev/null &
elif command -v open > /dev/null; then
    # macOS
    echo -e "${ROCKET}${GREEN} Opening NutriVeda Dashboard...${NC}"
    sleep 2
    open "http://localhost:8080/main_dashboard.html" 2>/dev/null &
fi

echo ""
echo -e "${LOTUS}${CYAN} Welcome to NutriVeda - Ancient Wisdom, Modern Technology!${NC}"
echo ""
echo -e "${YELLOW}⚠️  Press Ctrl+C to stop all services and exit...${NC}"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo -e "${YELLOW}🛑 Stopping NutriVeda services...${NC}"
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    
    # Wait a moment for graceful shutdown
    sleep 2
    
    # Force kill if still running
    kill -9 $BACKEND_PID 2>/dev/null
    kill -9 $FRONTEND_PID 2>/dev/null
    
    echo -e "${CHECK}${GREEN} All services stopped successfully${NC}"
    echo ""
    echo -e "${LOTUS}${CYAN} Thank you for using NutriVeda!${NC}"
    exit 0
}

# Set trap to cleanup on Ctrl+C
trap cleanup INT

# Wait for user to stop the servers
wait
