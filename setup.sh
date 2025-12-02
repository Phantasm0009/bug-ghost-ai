#!/bin/bash

echo "🚀 Setting up Bug Ghost AI..."

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check prerequisites
echo -e "${BLUE}Checking prerequisites...${NC}"

if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}Python 3 not found. Please install Python 3.11+${NC}"
    exit 1
fi

if ! command -v node &> /dev/null; then
    echo -e "${YELLOW}Node.js not found. Please install Node.js 18+${NC}"
    exit 1
fi

if ! command -v psql &> /dev/null; then
    echo -e "${YELLOW}PostgreSQL not found. You can use Docker Compose instead.${NC}"
fi

echo -e "${GREEN}✓ Prerequisites check complete${NC}\n"

# Setup backend
echo -e "${BLUE}Setting up backend...${NC}"
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
if [ ! -f .env ]; then
    cp .env.example .env
    echo -e "${YELLOW}⚠ Please edit backend/.env with your API keys${NC}"
fi

cd ..
echo -e "${GREEN}✓ Backend setup complete${NC}\n"

# Setup frontend
echo -e "${BLUE}Setting up frontend...${NC}"
cd frontend

# Install dependencies
npm install

# Copy environment file
if [ ! -f .env.local ]; then
    cp .env.example .env.local
fi

cd ..
echo -e "${GREEN}✓ Frontend setup complete${NC}\n"

# Final instructions
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✓ Setup complete!${NC}"
echo -e "${GREEN}========================================${NC}\n"

echo -e "Next steps:"
echo -e "1. Edit ${YELLOW}backend/.env${NC} with your LLM API key"
echo -e "2. Create PostgreSQL database: ${YELLOW}createdb bug_ghost_ai${NC}"
echo -e "3. Start backend: ${YELLOW}cd backend && source venv/bin/activate && uvicorn app.main:app --reload${NC}"
echo -e "4. Start frontend: ${YELLOW}cd frontend && npm run dev${NC}"
echo -e "\nOr use Docker Compose: ${YELLOW}docker-compose up${NC}\n"
