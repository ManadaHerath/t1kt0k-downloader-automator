#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo -e "${BLUE}======================================${NC}"
echo -e "${BLUE}  TikTok Telegram Bot Launcher${NC}"
echo -e "${BLUE}======================================${NC}\n"

if [ ! -f .env ]; then
    echo -e "${YELLOW}No .env file found. Creating one...${NC}\n"
    
    echo "To get your bot token:"
    echo "1. Open Telegram and search for @BotFather"
    echo "2. Send /newbot and follow the instructions"
    echo "3. Copy the token you receive"
    echo ""
    
    read -p "Enter your Telegram Bot Token: " BOT_TOKEN
    
    if [ -z "$BOT_TOKEN" ]; then
        echo -e "${RED}No token provided. Exiting...${NC}"
        exit 1
    fi
    
    echo "TELEGRAM_BOT_TOKEN=$BOT_TOKEN" > .env
    echo -e "${GREEN}Token saved to .env file${NC}\n"
fi

if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
    echo -e "${GREEN}Loaded environment variables from .env${NC}"
fi

if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
    echo -e "${RED}TELEGRAM_BOT_TOKEN not found in .env file${NC}"
    echo -e "${YELLOW}Please add your token to the .env file:${NC}"
    echo "TELEGRAM_BOT_TOKEN=your_token_here"
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}Python 3 found${NC}"

echo -e "${BLUE}Checking dependencies...${NC}"
if ! python3 -c "import telegram" 2>/dev/null; then
    echo -e "${YELLOW}Dependencies not installed. Installing...${NC}"
    pip3 install -r requirements.txt
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}Failed to install dependencies${NC}"
        exit 1
    fi
    echo -e "${GREEN}Dependencies installed${NC}"
else
    echo -e "${GREEN}Dependencies already installed${NC}"
fi

if [ ! -d "downloads" ]; then
    mkdir downloads
    echo -e "${GREEN}Created downloads directory${NC}"
fi

echo ""
echo -e "${GREEN}Starting Telegram Bot...${NC}"
echo -e "${YELLOW}Press Ctrl+C to stop the bot${NC}"
echo ""

python3 telegram_bot.py
