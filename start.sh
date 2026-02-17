#!/bin/bash
# YAAN Startup Script for Linux/Mac
# Run this to start the YAAN backend server

echo "╔═══════════════════════════════════════════╗"
echo "║                                           ║"
echo "║   ██╗   ██╗ █████╗  █████╗ ███╗   ██╗   ║"
echo "║   ╚██╗ ██╔╝██╔══██╗██╔══██╗████╗  ██║   ║"
echo "║    ╚████╔╝ ███████║███████║██╔██╗ ██║   ║"
echo "║     ╚██╔╝  ██╔══██║██╔══██║██║╚██╗██║   ║"
echo "║      ██║   ██║  ██║██║  ██║██║ ╚████║   ║"
echo "║      ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝   ║"
echo "║                                           ║"
echo "║     Your AI Assistant Network v1.0.0     ║"
echo "║          Offline • Private • Yours       ║"
echo "║                                           ║"
echo "╚═══════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 not found! Please install Python 3.10+${NC}"
    echo -e "${YELLOW}Install with: sudo apt install python3 python3-pip python3-venv${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Python found: $(python3 --version)${NC}"

# Check if virtual environment exists
VENV_PATH="./backend/venv"
if [ ! -d "$VENV_PATH" ]; then
    echo -e "${YELLOW}⚙️  Creating virtual environment...${NC}"
    cd backend
    python3 -m venv venv
    cd ..
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${GREEN}✓ Virtual environment exists${NC}"
fi

# Activate virtual environment and install dependencies
echo -e "${YELLOW}⚙️  Activating virtual environment...${NC}"
cd backend
source venv/bin/activate

# Check if dependencies are installed
if [ ! -f "venv/installed.flag" ]; then
    echo -e "${YELLOW}⚙️  Installing dependencies...${NC}"
    pip install --upgrade pip
    pip install -r requirements.txt
    touch venv/installed.flag
    echo -e "${GREEN}✓ Dependencies installed${NC}"
else
    echo -e "${GREEN}✓ Dependencies already installed${NC}"
fi

# Create necessary directories
mkdir -p data logs static

echo ""
echo -e "${GREEN}╔══════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║     🚀 Starting YAAN Server...          ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}📡 Server will be available at:${NC}"
echo -e "${GREEN}   http://localhost:8000${NC}"
echo ""
echo -e "${YELLOW}💡 Press Ctrl+C to stop the server${NC}"
echo ""

# Start the server
python main.py

# Deactivate on exit
deactivate
