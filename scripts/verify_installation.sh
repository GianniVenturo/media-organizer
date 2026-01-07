#!/bin/bash

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "=== Media Organizer Installation Verification ==="
echo ""

# Function to check command
check_command() {
    if command -v $1 &> /dev/null; then
        echo -e "${GREEN}✓${NC} $1 is installed"
        return 0
    else
        echo -e "${RED}✗${NC} $1 is NOT installed"
        return 1
    fi
}

# Check system commands
echo "=== System Commands ==="
check_command python3.12
check_command ffmpeg
check_command fpcalc
check_command mediainfo
check_command git

echo ""
echo "=== Python Environment ==="

# Activate venv if not activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

echo -e "${GREEN}✓${NC} Virtual environment: $VIRTUAL_ENV"

echo ""
echo "=== Python Packages ==="

# Check Python packages
python << 'PYEOF'
import sys

packages = [
    'pydantic',
    'yaml',
    'loguru',
    'acoustid',
    'librosa',
    'mutagen',
    'pydub',
    'sklearn',
    'watchdog',
    'pyudev',
    'imagehash',
    'sqlalchemy',
    'musicbrainzngs',
    'requests',
    'PIL',
    'numpy',
    'pandas'
]

all_ok = True
for pkg in packages:
    try:
        __import__(pkg)
        print(f"✓ {pkg}")
    except ImportError:
        print(f"✗ {pkg} NOT installed")
        all_ok = False

sys.exit(0 if all_ok else 1)
PYEOF

if [ $? -ne 0 ]; then
    echo -e "${RED}Some Python packages are missing!${NC}"
    exit 1
fi

echo ""
echo "=== Project Structure ==="

# Check directories
dirs=("src" "docs" "config" "logs" "data" "tests" "scripts")
for dir in "${dirs[@]}"; do
    if [ -d "$dir" ]; then
        echo -e "${GREEN}✓${NC} $dir/"
    else
        echo -e "${RED}✗${NC} $dir/ NOT found"
    fi
done

echo ""
echo "=== Configuration Files ==="

# Check config files
files=("config/config.yaml" "requirements.txt" "README.md")
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} $file"
    else
        echo -e "${RED}✗${NC} $file NOT found"
    fi
done

echo ""
echo "=== Git Configuration ==="
if [ -d ".git" ]; then
    echo -e "${GREEN}✓${NC} Git repository initialized"
    if git remote -v | grep -q origin; then
        echo -e "${GREEN}✓${NC} GitHub remote configured"
    else
        echo -e "${YELLOW}⚠${NC} GitHub remote not yet configured"
    fi
else
    echo -e "${RED}✗${NC} Git repository not initialized"
fi

echo ""
echo "==================================="
echo -e "${GREEN}✓ Installation verification complete!${NC}"
