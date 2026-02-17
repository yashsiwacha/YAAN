#!/bin/bash
# YAAN One-Click Installer for Linux/Mac
# This script will install and set up YAAN automatically

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo "╔═══════════════════════════════════════════╗"
echo "║                                           ║"
echo "║         YAAN v1.0 - INSTALLER            ║"
echo "║     Your AI Assistant Network            ║"
echo "║                                           ║"
echo "╚═══════════════════════════════════════════╝"
echo ""

# Check if Python is installed
echo -e "${CYAN}[1/6] Checking Python installation...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 not found!${NC}"
    echo ""
    echo -e "${YELLOW}Please install Python 3.10+ with:${NC}"
    echo -e "${YELLOW}  Ubuntu/Debian: sudo apt install python3 python3-pip python3-venv${NC}"
    echo -e "${YELLOW}  MacOS: brew install python@3.10${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo -e "${GREEN}✓ Python found: $PYTHON_VERSION${NC}"

# Check Python version
PYTHON_MAJOR=$(python3 -c 'import sys; print(sys.version_info.major)')
PYTHON_MINOR=$(python3 -c 'import sys; print(sys.version_info.minor)')

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 10 ]); then
    echo -e "${RED}❌ Python 3.10+ required, found: $PYTHON_VERSION${NC}"
    exit 1
fi

# Check if git is installed
echo ""
echo -e "${CYAN}[2/6] Checking Git installation...${NC}"
if command -v git &> /dev/null; then
    echo -e "${GREEN}✓ Git found${NC}"
else
    echo -e "${YELLOW}⚠️  Git not found (optional)${NC}"
fi

# Create virtual environment
echo ""
echo -e "${CYAN}[3/6] Creating virtual environment...${NC}"
VENV_PATH="./backend/venv"

if [ -d "$VENV_PATH" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment already exists, skipping...${NC}"
else
    python3 -m venv "$VENV_PATH"
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi

# Activate virtual environment and install dependencies
echo ""
echo -e "${CYAN}[4/6] Installing dependencies...${NC}"
source "$VENV_PATH/bin/activate"

# Upgrade pip
python -m pip install --upgrade pip --quiet

# Install requirements
pip install -r ./backend/requirements.txt
echo -e "${GREEN}✓ All dependencies installed${NC}"

# Create necessary directories
echo ""
echo -e "${CYAN}[5/6] Setting up directories...${NC}"
mkdir -p ./backend/data ./backend/logs ./backend/models
echo -e "${GREEN}✓ Directories configured${NC}"

# Run tests
echo ""
echo -e "${CYAN}[6/6] Running tests...${NC}"
cd backend
if python test_setup.py; then
    echo -e "${GREEN}✓ All tests passed!${NC}"
else
    echo -e "${YELLOW}⚠️  Some tests failed, but installation is complete${NC}"
fi
cd ..

# Deactivate virtual environment
deactivate

# Installation complete
echo ""
echo "╔═══════════════════════════════════════════╗"
echo "║                                           ║"
echo "║     ✅ YAAN INSTALLED SUCCESSFULLY!       ║"
echo "║                                           ║"
echo "╚═══════════════════════════════════════════╝"
echo ""
echo -e "${CYAN}🚀 Quick Start:${NC}"
echo -e "   Run:  ${GREEN}./start.sh${NC}"
echo -e "   Then open: ${GREEN}http://localhost:8000${NC}"
echo ""
echo -e "${CYAN}📚 Documentation:${NC}"
echo "   README.md - Full documentation"
echo "   QUICKSTART.md - 5-minute guide"
echo ""
echo -e "${CYAN}💡 Need help? Check the docs or visit:${NC}"
echo "   https://github.com/yashsiwacha/YAAN"
echo ""

# Make start script executable
chmod +x start.sh
echo -e "${GREEN}✓ Made start.sh executable${NC}"
